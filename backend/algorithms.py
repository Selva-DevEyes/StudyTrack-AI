"""
Handwritten algorithms module for StudyTrack AI.
Implements Insertion Sort, Binary Search, and Roster Aggregation without forbidden built-ins.
"""

from typing import List, Dict, Any, Union


def insertion_sort_by_field(students: List[Union[Dict[str, Any], Any]], field: str) -> List[Union[Dict[str, Any], Any]]:
    """
    Handwritten Insertion Sort algorithm.
    Sorts a list of student dicts or SQLAlchemy objects by field ('age' or 'name') in ascending order.
    
    Requirements:
    - Manual implementation
    - Outer loop starting from index 1
    - Visible while loop shifting larger elements right
    - Place the key element
    - Ascending order
    - NO calls to sorted() or .sort()
    """
    # Helper to get field value safely whether item is dict or object
    def get_val(item, f):
        if isinstance(item, dict):
            return item[f]
        return getattr(item, f)

    # Create a shallow copy to avoid mutating caller's original list in-place unexpectedly
    arr = list(students)
    n = len(arr)

    # Outer loop starting from index 1
    for i in range(1, n):
        key_item = arr[i]
        key_val = get_val(key_item, field)
        j = i - 1

        # Visible while loop shifting larger elements right
        while j >= 0 and get_val(arr[j], field) > key_val:
            arr[j + 1] = arr[j]
            j -= 1

        # Place key item in correct sorted position
        arr[j + 1] = key_item

    return arr


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


def format_roster_report(students: List[Union[Dict[str, Any], Any]], min_age: int) -> str:
    """
    Generates a structured text report summarizing roster metrics and eligible students.
    """
    def get_name(item):
        return item["name"] if isinstance(item, dict) else getattr(item, "name")

    def get_age(item):
        return item["age"] if isinstance(item, dict) else getattr(item, "age")

    def get_email(item):
        return item["email"] if isinstance(item, dict) else getattr(item, "email")

    total_count = len(students)
    qualifying_count = count_students_meeting_min_age(students, min_age)

    report_lines = [
        "============================================",
        "          STUDYTRACK ROSTER REPORT          ",
        "============================================",
        f"Total Registered Students: {total_count}",
        f"Filter Criterion: Minimum Age >= {min_age}",
        f"Qualifying Students Count: {qualifying_count}",
        "--------------------------------------------",
        "Qualifying Students List:"
    ]

    qualifying_students = [s for s in students if get_age(s) >= min_age]
    if not qualifying_students:
        report_lines.append("  (No students meet the specified age threshold)")
    else:
        for s in qualifying_students:
            report_lines.append(f"  • {get_name(s)} | Age: {get_age(s)} | Email: {get_email(s)}")

    report_lines.append("============================================")
    return "\n".join(report_lines)
