from datetime import date

def is_there_overlap(start1,end1,start2,end2):
    end1 = end1 or date.today()
    end2 = end2 or date.today()
    return start1 < end2 and start2 <end1

def is_there_shirt_number_overlap(start1,end1,start2,end2):
    end1 = end1 or date.today()
    end2 = end2 or date.today()
    return start1 <=end2 and start2<=end1