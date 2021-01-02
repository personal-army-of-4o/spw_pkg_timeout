-- tb top wrapper for spw_pkg_timeout

library ieee;
use ieee.std_logic_1164.all;


entity tb_top is
    port (
        iClk: in std_logic;
        iReset: in std_logic;

        iTimeout_ticks: in std_logic_vector (31 downto 0);

        iValid: in std_logic;
        iData: in std_logic_vector (8 downto 0);
        oAck: out std_logic;

        oValid: out std_logic;
        oData: out std_logic_vector (8 downto 0);
        iAck: in std_logic
    );
end entity;

architecture v1 of tb_top is

    constant cPipelined_impl: boolean := false;

    component spw_pkg_timeout
        generic (
            gPipelined_impl: boolean
        );
        port (
            iClk: in std_logic;
            iReset: in std_logic;

            iTimeout_ticks: in std_logic_vector;

            iValid: in std_logic;
            iData: in std_logic_vector (8 downto 0);
            oAck: out std_logic;

            oValid: out std_logic;
            oData: out std_logic_vector (8 downto 0);
            iAck: in std_logic
        );
    end component;

begin

    logic_top: spw_pkg_timeout
        generic map (
            gPipelined_impl => cPipelined_impl
        )
        port map (
            iClk => iClk,
            iReset => iReset,

            iTimeout_ticks => iTimeout_ticks,

            iValid => iValid,
            iData => iData,
            oAck => oAck,

            oValid => oValid,
            oData => oData,
            iAck => iAck
        );

end v1;
