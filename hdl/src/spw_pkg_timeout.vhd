-- truncate pkg if iTimeout_ticks have elapsed since last symbol
-- fsm:
-- 1. idle, wait for first symbol
-- 2. get a symbol, reset timer
-- 3. if symbol is EOP/EEP then goto 1, else goto 2
-- 4. if timeout, then send EEP, discard pkg tail, goto 1

library ieee;
use ieee.std_logic_1164.all;


entity spw_pkg_timeout is
	port (
		iClk           : in  std_logic;
		iReset         : in  std_logic;

		iTimeout_ticks : in  std_logic_vector (31 downto 0);

		iValid         : in  std_logic;
		iData          : in  std_logic_vector (8 downto 0);
		oAck           : out std_logic;

		oValid         : out std_logic;
		oData          : out std_logic_vector (8 downto 0);
		iAck           : in  std_logic
	);
end entity;

-- Dummy architecture to test with cocotb
architecture behavior of spw_pkg_timeout is
begin
  process (iClk, iReset) begin
    if (iReset = '1') then
      oAck   <= '0';
      oValid <= '0';
      oData  <= "000000000";
    elsif rising_edge(iClk) then
      oAck   <= '0';
      oValid <= '0';
      if (iValid = '1') then
        oData  <= iData;
        oValid <= '1';
        oAck   <= '1';
      end if;
    end if;
  end process;
end behavior;
