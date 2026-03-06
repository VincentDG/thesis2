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

    
def concurrency_mapping_summary(concurrency_list, grouped_linear_orders):
    c_no = 0
    for concurrency in concurrency_list:
        grp_no, trace_no, indices = concurrency[0], concurrency[1], concurrency[2]
        linear_order = grouped_linear_orders[grp_no][trace_no]
        concurrent_events = []
        print("Concurrency no: ", c_no)
        print(" " * 2, "Linear Order: ", grouped_linear_orders[grp_no][trace_no])
        print(" " * 2, "Indices: ", indices)
    
        for c_index in indices:
            event_no = linear_order[c_index]
            print(" "*2, "Concurrent event: ", event_no)
            concurrent_events.append(event_no)

        print(" " * 2, "Concurrent events: ", concurrent_events )

def permutation_summary(p):
    print(" " * 4, "Permutations of Current Events: ")

    for permutation in p:
        print(" " * 6, permutation)

def linear_extension_summary(linear_extensions):
    print(" "*4, "Linear Extensions:")
    for extension in linear_extensions:
        print(" "*6, extension)

def lo_strings_summary(lo_strings):
    print(" "*4, "Linear Order Strings")
    
    g = 0
    for grp in lo_strings:
        c = 0
        print(" "*2, "Group no: ", g)
        for s in grp:
            print(" "*4, s)
            if c >= BREAK_NO:
                print(" "*6, "...", len(grp)-BREAK_NO, "more entries")
                break
            c += 1
        # if g >= BREAK_NO:
        #     print(" "*2, "...", len(lo_strings)-BREAK_NO, "more groups")
        #     break
        g += 1


def output_upsilon(lo_strings):
    for grp in lo_strings:
        for s in grp:
            print(s)
        print()

# This section of the code is for printing and testing outputs
def print_adj_matrix(
    adj_matrix: list[list[int]]
):
    for row in adj_matrix:
        print(" "*4, row)

def print_poset_cover(
    poset_cover: list[list[list[int]]]
):
    for i in range(len(poset_cover)):
        print(" "*2, "Poset number: ", i)
        print_adj_matrix(poset_cover[i])

def print_poset_block(
    master_list: list[list[list[list[int]]]]  #check how to define classes later
):
    for i in range(len(master_list)):
        print("Posets for string group no: ", i)
        print_poset_cover(master_list[i])

def result_poset_summary(result_posets, grp_no):
    print("Posets for group no: ", grp_no)
    poset_number = 0
    for poset in result_posets:
        print(" "*2, "Poset number: ", poset_number)
        print(" "*4, poset)
        poset_number += 1
    print("---")