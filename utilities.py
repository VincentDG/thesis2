BREAK_NO = 6

def event_sets_summary(event_sets):
    valid = 0
    for event_set in event_sets:
        if len(event_set) >= 2 and len(event_set) <=6:
            valid = valid + 1
        print(event_set, len(event_set))

    print("Number of sets:", len(event_sets))
    print("Valid sets:", valid)

def grp_traces_summary(grp_traces):
    print("Length of grp_traces:", len(grp_traces))
    sum = 0
    for trace in grp_traces:
        sum += len(trace)

    print("Number of recorded events:", sum)

def co_grp_summary(co_grp_traces):
    print("---")
    print("Chronologically Ordered Groups:")
    group_no = 0
    for group in co_grp_traces:
        print(" "*2, "Group no:", group_no + 1)
        # trace_no = 0
        # for trace in group:
            # print(" "*4, "Trace no:", trace_no + 1)
            # for event in trace:
            #     print(" "*6, event[0])
        #     trace_no += 1

        #     if trace_no >= BREAK_NO:
        #         print(" "*6, "...", len(group) - BREAK_NO, "more entries")
        #         break
        print(" "*6, "Traces in group: ", len(group))
        print(" "*2, "------")
        group_no += 1
        
        # if trace_no >= BREAK_NO:
        #     break
    print("No. of chronologically ordered groups:", len(co_grp_traces))

def event_dict_summary(event_dict):
    print("---")
    print("Event Dictionary:")
    for key in event_dict:
        value = event_dict[key]
        print(" "*2, key, ":", value)

def concurrent_event_checker(event_dict, concurrency_list, co_grp_traces, grouped_linear_orders):
    """
    This function checks the corresponding trace for the concurrent event

    Format of concurrency on concurrency list:
        [grp_index, trace_index, event_index_1, event_index_2]
    """
    print("---")
    print("Concurrent Event Checker")
    concurrency_no = 0
    for concurrency in concurrency_list:
        grp_index, trace_index, event_index_1, event_index_2 = concurrency[0], concurrency[1], concurrency[2], concurrency[3]

        print("Concurrency: ", concurrency)
        print("Chronologically ordered group:", grp_index)
        print("Trace number:", trace_index)

        trace = co_grp_traces[grp_index][trace_index]
        
        print("--------------- TRACE BREAKDOWN ---------------")
        event_no = 0
        for event in trace:
            if event_no == event_index_1 or event_no == event_index_2:
                print(f"{event[0]:<20} [{event_dict[event[0]]}] \t {event[1]} <-- CONCURRENT EVENT")
            else:
                print(f"{event[0]:<20} [{event_dict[event[0]]}] \t {event[1]}")

            event_no += 1
        print("---")
        concurrency_no += 1

        # Linear order equivalent
        print("Linear order: ", grouped_linear_orders[grp_index][trace_index])
        print()



        # if concurrency_no >= BREAK_NO:
        #     break

def concurrency_list_summary(concurrency_list):
    print("---")
    print("Concurrency List")
    concurrency_no = 0
    # Group Index, Trace Index, Event Index 1, Event Index 2

    for concurrency in concurrency_list:
        print(" "*2, concurrency_no, ":", concurrency)
        concurrency_no += 1

        if concurrency_no >= BREAK_NO:
            print(" "*4, "...", len(concurrency_list) - BREAK_NO, "more concurrencies")
            break
    
    print("Number of concurrencies: ", len(concurrency_list))

def linear_order_summary(linear_orders):
    print("---")
    print("Linear Orders")
    linear_order_no = 0
    for linear_order in linear_orders:
        print(" "*2, linear_order_no + 1, ":" ,linear_order)
        linear_order_no += 1

        if linear_order_no >= BREAK_NO:
            break

    print("Number of linear orders: ", len(linear_orders))

def grouped_linear_order_summary(grouped_linear_orders):
    print("---")
    print("Grouped Linear Orders")
    print("Number of linear order groups: ", len(grouped_linear_orders))
    group_no = 0
    valid_count = 0
    for group in grouped_linear_orders:
        print(" "*2, "Group no:", group_no)
        linear_order_no = 0
        for linear_order in group:
            print(" "*4, linear_order)
            linear_order_no += 1
            if linear_order_no >= BREAK_NO:
                print(" "*4, "...", len(group) - BREAK_NO, "more entries")
                break
        print(" "*2, "Number of ")
        trace = group[0]
        if len(trace) >= 2 and len(trace) <= 6:
            valid_count += 1

        print(" "*6, "Traces in group: ", len(group))
        print(" "*6, "Number of events in group: ", len(group[0]))
        print(" "*2, "------")
        group_no +=1
    print("No. of chronologically ordered groups:", len(grouped_linear_orders))
    print("Number of valid groups: ", valid_count)

    

        


