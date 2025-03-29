rule Packed_Executable {
    meta:
        description = "Detects common packers and cryptors"
        author = "MalHunter Team"
        date = "2023-11-15"
    
    strings:
        $upx = "UPX!" fullword
        $aspack = "ASPack" fullword
        $fsg = "FSG!" fullword
        $pecompact = "PEC2" fullword
        $petite = "Petite" fullword
        $mew = "MEW" fullword
        $upack = "UPACK" fullword
        $nspack = "NSPACK" fullword
        $kkrunchy = "kkrunchy" fullword
    
    condition:
        uint16(0) == 0x5A4D and any of them
}
