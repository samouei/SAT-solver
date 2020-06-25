#!/usr/bin/env python3
"""6.009 Lab 5 -- Boolean satisfiability solving"""

import sys
sys.setrecursionlimit(10000)
# NO ADDITIONAL IMPORTS



def make_new_formula(formula, lit, lit_val):
    """
    Updates a CNF formula with the consequences of setting lit to lit_val.
    Parameters: 
        formula: list of clauses [ [(x, Bool)] ]
        lit: string
        lit_val: True or False
    Returns a modified CNF formula.
    """
    
    new_formula = []
    for c in formula:  
        
        # remove all the clauses with the literal
        if (lit, lit_val) not in c:
            new_formula.append(c.copy())
            
            # update the remaining clasues with (lit, not lit_val)
            while (lit, not lit_val) in new_formula[-1]:
                new_formula[-1].remove((lit, not lit_val)) 
    return new_formula
    
    

def satisfying_assignment(formula):
    """
    Find a satisfying assignment for a given CNF formula.
    Returns that assignment if one exists, or None otherwise.

    >>> satisfying_assignment([])
    {}
    >>> x = satisfying_assignment([[('a', True), ('b', False), ('c', True)]])
    >>> x.get('a', None) is True or x.get('b', None) is False or x.get('c', None) is True
    True
    >>> satisfying_assignment([[('a', True)], [('a', False)]])
    """
    
    # Base Case 
    if not formula:
        return {}
    
    if any(len(i) == 0 for i in formula):  
        return None
    
    # Sort and always take the first one (to get all unit clauses first)
    sorted_formula = sorted(formula, key = len) 
    lit = sorted_formula[0][0][0]


   	######### Part1: searching for unit clauses #########   
         
    if len(sorted_formula[0]) == 1:
         
        lit = sorted_formula[0][0][0]
        lit_val = sorted_formula[0][0][1]

        new_formula = make_new_formula(formula, lit, lit_val)

        # Check for any empty clasues
        if any(len(i) == 0 for i in new_formula):  
            return None  
        
        result = satisfying_assignment(new_formula)
        if result != None:              
        		return {**result, **{lit: lit_val}} 
        else:
          return None

     
   	######### Part2: setting x to True #########
       
    new_formula = make_new_formula(formula, lit, True)
            
    result = satisfying_assignment(new_formula)
    if result != None:              
        return {**result, **{lit: True}} 


    ######### Part3: setting x to False #########

    new_formula = make_new_formula(formula, lit, False)

    result = satisfying_assignment(new_formula)
    if result != None:                     
        return {**result, **{lit: False}}


    return None

   
def create_room_pairs(session_capacities):
    """
    Creates all size 2 combinations of rooms.
    Parameters: 
        session_capacities: a dictionary mapping each session name to a positive
                        integer for how many students can fit in that session
    Returns a set of room pairings (tuples).
    """    
    
    sessions = [s for s in session_capacities]
    pairs = {(sessions[i], j) for i in range(len(sessions)) for j in sessions[i:] if sessions[i] != j}
    return pairs

    
def size_k_combinations(iterable, k):
    """
    Creates all size k combinations of elements.
    Parameters: 
        iterable: a dictionary mapping 
    Returns a list of size k combinations (tuples).
    """     
    
    item_list = [k for k in iterable]
    if k == 0:
        return [tuple()]
    
    if len(iterable) < k:
        return []
    
    if len(iterable) == k:
    	return [tuple(iterable)]
        
    # with first element
    result = [(item_list[0],) + c for c in size_k_combinations(item_list [1:], k - 1)]
    # without first element
    result += size_k_combinations(item_list[1:], k)
        
    return result

    
def boolify_scheduling_problem(student_preferences, session_capacities):
    """
    Convert a quiz-room-scheduling problem into a Boolean formula.

    student_preferences: a dictionary mapping a student name (string) to a set
                         of session names (strings) that work for that student
    session_capacities: a dictionary mapping each session name to a positive
                        integer for how many students can fit in that session

    Returns: a CNF formula encoding the scheduling problem, as per the
             lab write-up
    We assume no student or session names contain underscores.
    """
    
    # Creating room pairs
    room_pairs = size_k_combinations(session_capacities, 2)
    
    desired_rooms_rule = [] # room preferences 
    one_session_rule = [] # student in at most one session
    room_capacity_rule = [] # no oversubscribed sections
    
    for s in student_preferences:
        
        # Encoding rule 1: Students Only In Desired Rooms 
        student_room_preference = []
        
        # Add student's desired room(s)
        for r in student_preferences[s]: 
            student_room_preference.append((s + "_" + str(r), True)) # (student_desiredRoom, True)
        desired_rooms_rule.append(student_room_preference)
        
        
        # Encoding rule 2: Each Student In Exactly One Session 
        for rp in room_pairs:
            student_room_combo = []
            for r in rp:
                student_room_combo.append((s + "_" + str(r), False)) # (student_Room, False) *for each room pair*
            one_session_rule.append(student_room_combo) 
        
        
    # Encoding rule 3: No Oversubscribed Sections 
    for r in session_capacities:
        
        # Create size room_capacity + 1 combinations/groups of students
        for student_combo in size_k_combinations(student_preferences, session_capacities[r] + 1):
            room_capacities = []
            for s in student_combo:
                room_capacities.append((s + "_" + str(r), False)) # (student_Room, False) 
            room_capacity_rule.append(room_capacities)
    
    
    # Combine all the rules        
    CNF = desired_rooms_rule + one_session_rule + room_capacity_rule
    return CNF
        
    
if __name__ == '__main__':
    import doctest
    _doctest_flags = doctest.NORMALIZE_WHITESPACE | doctest.ELLIPSIS
    doctest.testmod(optionflags=_doctest_flags)
    
#    session_capacities = {'basement': 1,'kitchen': 2,'penthouse': 4}       
#    print(create_room_pairs(session_capacities))  
#    
#    
#    session_capacities = {'Alice': {'basement', 'penthouse'},
#                            'Bob': {'kitchen'},
#                            'Charles': {'basement', 'kitchen'},
#                            'Dana': {'kitchen', 'penthouse', 'basement'}}   
#    print(size_k_combinations(session_capacities, 3))
#    
#
##Rule 1
#[ 
# [('Alice_basement', True), ('Alice_penthouse', True)], 
# [('Bob_kitchen', True)],
# [('Charles_basement', True), ('Charles_kitchen', True)],
# [('Dana_kitchen', True), ('Dana_penthouse', True), ('Dana_basement', True)]
#]
#
#
##Rule 2
#[ 
#  [('Alice_basement', False), ('Alice_penthouse', False)], 
#  [('Alice_basement', False), ('Alice_kitchen', False)], 
#  [('Alice_penthouse', False), ('Alice_kitchen', False)],
#  
#  [('Bob_basement', False), ('Bob_penthouse', False)], 
#  [('Bob_basement', False), ('Bob_kitchen', False)],
#  [('Bob_penthouse', False), ('Bob_kitchen', False)],
#  
#  [('Charles_basement', False), ('Charles_penthouse', False)], 
#  [('Charles_basement', False), ('Charles_kitchen', False)], 
#  [('Charles_penthouse', False), ('Charles_kitchen', False)], 
# 
#  [('Dana_basement', False), ('Dana_penthouse', False)], 
#  [('Dana_basement', False), ('Dana_kitchen', False)], 
#  [('Dana_penthouse', False), ('Dana_kitchen', False)] 
#]
#
#
##Rule 3
##basement, kitchen
#[
# [('Bob_basement', False), ('Alice_basement', False)],
# [('Bob_basement', False), ('Charles_basement', False)],
# [('Bob_basement', False), ('Dana_basement', False)],
# [('Alice_basement', False), ('Charles_basement', False)],
# [('Alice_basement', False), ('Dana_basement', False)],
# [('Charles_basement', False), ('Dana_basement', False)],
# 
# [('Bob_kitchen', False), ('Alice_kitchen', False), ('Charles_kitchen', False)],
# [('Bob_kitchen', False), ('Alice_kitchen', False), ('Dana_kitchen', False)],
# [('Bob_kitchen', False), ('Charles_kitchen', False), ('Dana_kitchen', False)],
# [('Alice_kitchen', False), ('Charles_kitchen', False), ('Dana_kitchen', False)]
#]

