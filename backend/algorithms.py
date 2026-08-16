"""
Handwritten algorithms module for StudyTrack AI.
Implements Insertion Sort (O(N^2)), Binary Search (O(log N)), and Roster Aggregation.
All algorithms are handwritten without relying on forbidden Python built-ins.
"""

from typing import List, Dict, Any, Union


def insertion_sort_by_field(students: List[Union[Dict[str, Any], Any]], field: str) -> List[Union[Dict[str, Any], Any]]:
    """
    Handwritten Insertion Sort algorithm (in-place modification).
    Sorts the passed-in list of student dicts or SQLAlchemy objects by field ('age' or 'name') in ascending order.
    
    Requirements:
    - In-place mutation of input list
    - Manual implementation
    - Outer loop starting from index 1
    - Visible while loop shifting larger elements right
    - Place the key element
    - Ascending order
    - NO calls to sorted() or .sort() inside function body
    """
    def get_val(item, f):
        if isinstance(item, dict):
            return item[f]
        return getattr(item, f)

    for i in range(1, len(students)):
        key_item = students[i]
        key_val = get_val(key_item, field)
        j = i - 1

        # Visible while loop shifting larger elements right
        while j >= 0 and get_val(students[j], field) > key_val:
            students[j + 1] = students[j]
            j -= 1

        # Place key item in correct sorted position
        students[j + 1] = key_item

    return students


def binary_search_by_name(sorted_by_name_list: List[Union[Dict[str, Any], Any]], name: str) -> Union[Dict[str, Any], Any, int]:
    """
    Iterative Binary Search for a student by exact name in a name-sorted list.
    
    Requirements:
    - Iterative implementation
    - Overflow-safe midpoint calculation: mid = low + (high - low) // 2
    - Return student object/dict when found
    - Return -1 when not found
    """
    def get_name(item):
        if isinstance(item, dict):
            return item["name"]
        return getattr(item, "name")

    low = 0
    high = len(sorted_by_name_list) - 1
    target_name = name.strip()

    while low <= high:
        # Overflow-safe midpoint calculation as specified
        mid = low + (high - low) // 2
        mid_name = get_name(sorted_by_name_list[mid])

        if mid_name == target_name:
            return sorted_by_name_list[mid]
        elif mid_name < target_name:
            low = mid + 1
        else:
            high = mid - 1

    return -1


def count_students_meeting_min_age(students: List[Union[Dict[str, Any], Any]], min_age: int) -> int:
    """
    Counts students meeting or exceeding min_age using an explicit loop.
    
    Requirements:
    - Do NOT collapse into a bare one-line sum(...)
    """
    def get_age(item):
        if isinstance(item, dict):
            return item["age"]
        return getattr(item, "age")

    count = 0
    for student in students:
        if get_age(student) >= min_age:
            count += 1
    return count


def format_roster_report(students: List[Union[Dict[str, Any], Any]]) -> str:
    """
    Formats the student roster into a string report with one line per student:
    "[Age {age}] {name} <{email}>"
    """
    lines = []
    for s in students:
        name = s["name"] if isinstance(s, dict) else getattr(s, "name")
        age = s["age"] if isinstance(s, dict) else getattr(s, "age")
        email = s["email"] if isinstance(s, dict) else getattr(s, "email")
        lines.append(f"[Age {age}] {name} <{email}>")
    return "\n".join(lines)
