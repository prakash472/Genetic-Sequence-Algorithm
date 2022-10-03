import numpy as np
import psutil
import sys
file_path=sys.argv[1]

# collecting the input from text_file
def fileProcessing():
    with open(file_path) as f:
        lines=f.readlines()
    first_string=lines[0].rstrip("\n")
    first_pattern=[]
    second_pattern=[]
    second_pattern_position=0
    for i in range(1,len(lines)):
        line_item=lines[i].rstrip("\n")
        if line_item.isnumeric():
            first_pattern.append(int(line_item))
        else:
            second_string=line_item.rstrip("\n")
            second_pattern_position=i+1
            break
    for i in range(second_pattern_position,len(lines)):
        second_pattern.append(int(lines[i].rstrip("\n")))
    return first_string,first_pattern,second_string,second_pattern

# generating the input
def generateInputString(sequence,pattern):
    result=sequence
    i=0
    for position in pattern:
        result=result[:position+1]+result+result[position+1:len(result)]
    return result

# Calculating the Sequence Algnment
def calculateSequenceAlignmentMatrix(first_generated_string,second_generated_string):
    m,n=len(first_generated_string),len(second_generated_string)
    dp=[[-1 for i in range(m+1)] for j in range(n+1)]
    for i in range(len(dp)):
        for j in range(len(dp[0])):
            # INITIALIZATION OF DP MATRIX
            if i==0:
                dp[i][j]=j*gap_penalty
            if j==0:
                dp[i][j]=i*gap_penalty
    for i in range(1,len(dp)):
        for j in range(1,len(dp[0])):
            dp[i][j]=min(dp[i-1][j-1]+mismatch_penalty[(first_generated_string[j-1],second_generated_string[i-1])],
                        dp[i][j-1]+gap_penalty,
                        dp[i-1][j]+gap_penalty)
    return dp
# Backtracking to get the aligned string
def calculateAlignmentString(alignment_matrix,string1,string2):
    i,j=len(string2),len(string1)
    alignment_first=""
    alignment_second=""
    while i>0 and j>0:
        prev_val=min(alignment_matrix[i-1][j-1]+mismatch_penalty[(string1[j-1],string2[i-1])],
                            alignment_matrix[i][j-1]+gap_penalty,
                            alignment_matrix[i-1][j]+gap_penalty)
        if prev_val==alignment_matrix[i-1][j-1]+mismatch_penalty[(string1[j-1],string2[i-1])]:
            alignment_first+=string1[j-1]
            alignment_second+=string2[i-1]
            i-=1
            j-=1
        elif prev_val==alignment_matrix[i-1][j]+gap_penalty:
            alignment_first+="-"
            alignment_second+=string2[i-1]
            i-=1
        elif prev_val==alignment_matrix[i][j-1]+gap_penalty:
            alignment_first+=string1[j-1]
            alignment_second+="-"
            j-=1
    while j>0:
        alignment_first+=string1[j-1]
        alignment_second+="-"
        j-=1
    while i>0:
        alignment_first+="-"
        alignment_second+=string2[i-1]
        i-=1
    return(alignment_first[::-1],alignment_second[::-1])

if __name__=="__main__":
    first_string,first_pattern,second_string,second_pattern=fileProcessing()
    first_generated_string=generateInputString(first_string,first_pattern)
    second_generated_string=generateInputString(second_string,second_pattern)

    mismatch_penalty={
                    ("A","A"):0,  
                    ("A","C"):110,
                    ("A","G"):48,
                    ("A","T"):94,
                    ("C","A"):110,
                    ("C","C"):0,
                    ("C","G"):118,
                    ("C","T"):48,
                    ("G","A"):48,
                    ("G","C"):118,
                    ("G","G"):0,
                    ("G","T"):110,
                    ("T","A"):94,
                    ("T","C"):48,
                    ("T","G"):110,
                    ("T","T"):0
                    }
    gap_penalty=30
    if len(first_generated_string) <= 1024 and len(second_generated_string)<=1024:
        alignment_matrix=calculateSequenceAlignmentMatrix(first_generated_string,second_generated_string)
        best_score=alignment_matrix[-1][-1]
        alignment_first,alignment_second=calculateAlignmentString(alignment_matrix,first_generated_string,second_generated_string)
        alignment_first=alignment_first[:50]+" "+alignment_first[-50:]
        alignment_second=alignment_second[:50]+" "+alignment_second[-50:]

        memory_usage=psutil.Process().memory_info().rss / (1024)

        # psutil.Process().cpu_times() gives the tuple where the total time is user time[0] and the system time[1]
        cpu_usage=psutil.Process().cpu_times()[0]+psutil.Process().cpu_times()[1]
        with open("output.txt","w") as f:
            f.write("{}\n{}\n{}\n{}\n{}\n".format(alignment_first,alignment_second,str(best_score),str(cpu_usage),str(memory_usage)))
    else:
        print("Error in input")

