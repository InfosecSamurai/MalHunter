rule Suspicious_Behavior {
    meta:
        description = "Suspicious but not definitively malicious"
        author = "MalHunter Team"
    
    strings:
        $keylogger = "SetWindowsHookEx" nocase
        $screenshot = "BitBlt" nocase
        $hidden_window = "SW_HIDE" nocase
        $process_injection = "WriteProcessMemory" nocase
        $privilege_esc = "SeDebugPrivilege" nocase
    
    condition:
        2 of them
}

rule Obfuscated_Code {
    meta:
        description = "Potential code obfuscation"
    
    strings:
        $long_jmp = { E9 ?? ?? ?? ?? }
        $xor_loop = { 80 ?? ?? 00 75 ?? }
        $stack_string = { 68 ?? ?? ?? ?? }
    
    condition:
        any of them and #long_jmp > 5
}
