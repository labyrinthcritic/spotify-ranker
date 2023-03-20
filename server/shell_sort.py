def shell_sort(items):
    # initial value of the gap n / 2 
    size = len(items)
    gap = int(size / 2)

    # iterating until gap == 1 
    while gap > 0:
        # iterating through arr by gap size 
        for i in range(size): 
            slowNum = i 
            fastNum = i 

            # check if numbers are in range 
            if (fastNum + gap) < size:
                fastNum = i + gap

                # check to see if swap is required 
                if items[slowNum] > items[fastNum]:
                    temp = items[slowNum]
                    items[slowNum] = items[fastNum]
                    items[fastNum] = temp 

                    # checking to see if swaps before is required 
                    slowNum = slowNum - gap 
                    fastNum = fastNum - gap  

                    while (slowNum >= 0 and fastNum <= size): 
                       # swap required 
                       if items[slowNum] > items[fastNum]:
                            items[slowNum], items[fastNum] = items[fastNum], items[slowNum]

                            slowNum = slowNum - gap 
                            fastNum = fastNum - gap  
                       else:
                           break
        # after iterating through the array with the gap 
        # increment the gap --> incrementation from shell sort pseudocode slide 74
        if gap == 2:
            gap = 1
        else:
            gap = int(gap / 2)
