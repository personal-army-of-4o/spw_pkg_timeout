library work;
use work.json.all;

package config is

    constant cTimeout_ticks_width: natural;

end package;

package body config is

    constant cTimeout_tick_width_name: string := "timeout_cfg_width";
    constant cConfig_location: string := ".";
    constant cConfig_name: string := "config.json";
    constant cConfig_path: string := cConfig_location & "/" & cConfig_name;
    constant cConfig_str: T_JSON := jsonLoad (cConfig_path);

    function get_cfg (cfg: T_JSON) return natural is
        variable ret: natural;
    begin
        if jsonNoParserError (cfg) = false then
            assert false report jsonGetErrorMessage (cfg) severity failure;
        end if;
        return natural'value(jsonGetString(cfg, "timeout_reg_width"));
    end function;

    constant cTimeout_ticks_width: natural := get_cfg (cConfig_str);

end package body;

