-- truncate pkg if iTimeout_ticks have elapsed since last symbol
-- fsm:
-- 1. idle, wait for first symbol
-- 2. get a symbol, reset timer
-- 3. if symbol is EOP/EEP then goto 1, else goto 2
-- 4. if timeout, then send EEP, discard pkg tail, goto 1

library ieee;
use ieee.std_logic_1164.all;
use ieee.numeric_std.all;
library work;
use work.config.all;


entity spw_pkg_timeout is
    generic (
        gReset_active_lvl: std_logic := '0';
        gPipelined_impl: boolean := false
    );
    port (
        iClk: in std_logic;
        iReset: in std_logic;

        iTimeout_ticks: in std_logic_vector (cTimeout_ticks_width-1 downto 0);

        iValid: in std_logic;
        iData: in std_logic_vector (8 downto 0);
        oAck: out std_logic;

        oValid: out std_logic;
        oData: out std_logic_vector (8 downto 0);
        iAck: in std_logic
    );
end entity;

architecture v1 of spw_pkg_timeout is

    constant cCnt_w: natural := iTimeout_ticks'length;

    type tState is (idle, armed, send_eep, discard);

    signal sState: tState;
    signal sState_next: tState;
    signal sArmed_case_word: std_logic_vector (1 downto 0);
    signal sCnt_done: std_logic;
    signal sEp: std_logic;
    signal sAck: std_logic;
    signal sCnt_eq_tm: std_logic;
    signal sCnt_done_al: std_logic;
    signal sCnt: unsigned (cCnt_w-1 downto 0);

begin

    oAck <= sAck;

    sArmed_case_word <= sCnt_done & sEp;

    sEp <= '1' when iValid = '1' and iAck = '1' and iData = '1' & x"00" else '0';

    sCnt_done_al <= '0' when iTimeout_ticks = (cCnt_w-1 downto 0 => '0') else '1';
    sCnt_eq_tm <= sCnt_done_al when iTimeout_ticks = std_logic_vector(sCnt) else '0';

    process (iClk, iReset)
    begin
        if iReset = gReset_active_lvl then
            sCnt_done <= '0';
        else
            if iClk'event and iClk = '1' then
                sCnt_done <= sCnt_eq_tm;
            end if;
        end if;
    end process;

    process (iClk, iReset)
    begin
        if iReset = gReset_active_lvl then
            sCnt <= (others => '0');
        else
            if iClk'event and iClk = '1' then
                if sState = armed and iValid = '0' then
                    sCnt <= sCnt+1;
                else
                    sCnt <= (others => '0');
                end if;
            end if;
        end if;
    end process;

    process (sState, iValid, iAck, sArmed_case_word, sEp)
    begin
        sState_next <= sState;
        case sState is
            when idle =>
                if iValid = '1' then
                    sState_next <= armed;
                end if;
            when armed =>
                case sArmed_case_word is
                    when "01" | "11" =>
                        sState_next <= idle;
                    when "10" =>
                        sState_next <= send_eep;
                    when others =>
                end case;
            when send_eep =>
                if iAck = '1' then
                    sState_next <= discard;
                end if;
            when discard =>
                if sEp = '1' then
                    sState_next <= idle;
                end if;
            when others =>
        end case;
    end process;

    process (iClk, iReset)
    begin
        if iReset = gReset_active_lvl then
            sState <= idle;
        else
            if iClk'event and iClk = '1' then
                sState <= sState_next;
            end if;
        end if;
    end process;

    process (sState, iAck, iValid, iData)
    begin
        case sState is
            when idle =>
                oValid <= '0';
                oData <= '0' & x"00";
                sAck <= '0';
            when armed =>
                oValid <= iValid;
                oData <= iData;
                sAck <= iAck;
            when send_eep =>
                oValid <= '1';
                oData <= '1' & x"01";
                sAck <= '0';
            when discard =>
                oValid <= '0';
                oData <= '0' & x"00";
                sAck <= iValid;
            when others =>
        end case;
    end process;

end v1;
