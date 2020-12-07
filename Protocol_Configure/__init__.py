def Route_Switch(protocol,root_screen):
    if protocol == 'TUNL':
        import Protocol_Configure.TUNL as prca
    elif protocol == 'vPRL':
        import Protocol_Configure.vPRL as prca
    elif protocol == 'PAL':
        import Protocol_Configure.PAL as prca
    elif protocol == 'iCPT':
        import Protocol_Configure.iCPT as prca
    elif protocol == 'iCPT2':
        import Protocol_Configure.iCPT2 as prca
    elif protocol == 'iCPTImage2':
        import Protocol_Configure.iCPTImage2 as prca
    elif protocol == 'iCPTStimDurationScreen':
        import Protocol_Configure.iCPTStimDurationScreen as prca
    elif protocol == 'iCPTImageScreen':
        import Protocol_Configure.iCPTImageScreen as prca
    elif protocol == 'iCPTStimImageScreen':
        import Protocol_Configure.iCPTStimImageScreen as prca
    elif protocol == 'PR':
        import Protocol_Configure.PR as prca
    elif protocol == 'PR2':
        import Protocol_Configure.PR2 as prca

    prca.Experiment_Configuration(root_screen=root_screen)
