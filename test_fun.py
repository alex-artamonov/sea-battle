import pytest
import scratch as s

def test_contin_right():
    right = [(1,1), (1,2), (1,0)]
    right = [(0,3), (0,2), (0,1)]
    right = [(1,2), (2,2),(0,2)]
    size = 5
    right = [(0, i) for i in range(size)]
    print(right)
    
    assert s.is_line_continuous(right)

def test_contin_wrong():
    wrong = [(1,2), (1,4)]
    assert False == s.is_line_continuous(wrong)