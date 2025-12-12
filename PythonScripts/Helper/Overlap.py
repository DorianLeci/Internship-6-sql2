from datetime import date,timedelta

def is_there_overlap(start1,end1,start2,end2):
    end1 = end1 or date.today()+timedelta(days=365*10)
    end2 = end2 or date.today()+timedelta(days=365*10)

    return start1 < end2 and start2 <end1

def is_there_overlap_inclusive(start1,end1,start2,end2):
    end1 = end1 or date.today()+timedelta(days=365*10)
    end2 = end2 or date.today()+timedelta(days=365*10)

    return start1 <=end2 and start2<=end1

def has_current_captain(current_team_number,current_team_id,date_of_joining,date_of_departure):

    overlap=any(is_captain and is_there_overlap_inclusive(s,e,date_of_joining,date_of_departure) 
                for s,e,_,is_captain in current_team_number.get(current_team_id,[]))
    
    return overlap