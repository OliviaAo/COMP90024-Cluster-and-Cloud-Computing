 

'''
    Three libraries:
        1. mpi4py: MPI for Python
        2. json: include some function for loading the json files.
        3. time: for calculating the executing time for the program
'''
from mpi4py import MPI
import json
import time


starttime = time.time()
 
'''
    1.Create MPI communicator
      Rank: represents each node's ID, start from 0
      Size: represents the number of nodes in communicator
'''
comm = MPI.COMM_WORLD
comm_rank = comm.Get_rank()
comm_size = comm.Get_size()

'''
    2. Open the files:
       melbGrid.json: The data for gird boxes coordinates.
       xxxxTwitter.json: The coordinates data for twitter users 
'''
f1 = open("/Users/admin/Desktop/CloudComputing/Assignment/projectFiles/melbGrid.json", 'r')
f2 = open("/Users/admin/Desktop/CloudComputing/Assignment/projectFiles/smallTwitter.json", 'r')

'''
    3. Set magic number 16 and 4:
        1. We have 16 grid boxes in the melbGrid.json file
        2. For each grid box, it has xmin/xmax/ymin/ymax ---> 4 coordinates
'''
num_of_gridBox = 16
coordinates_of_gridBox = 4 

'''
    4. Load data for the grid box
       Coordi list store the gird box coordinates informations:
       For example:
           if there is a pointA[x,y], grid box B has[xmin,xmax,ymin,ymax]
               if  xmin<=x<=xmax and ymin<=y<=ymax --> pointA is in grid box B.
'''
data = json.load(f1)
f1.close()
coordi = [[0 for col in range(coordinates_of_gridBox)] for row in range(num_of_gridBox)]
i = 0
for feature in data['features']:
    coordi[i][0] = feature['properties']['xmin']
    coordi[i][1] = feature['properties']['xmax']
    coordi[i][2] = feature['properties']['ymin']
    coordi[i][3] = feature['properties']['ymax']
    i += 1

'''
    5. Parallel Calculate the tweets coordinates, judging if they are in grid box or not: 
       Set rank0 node as the master node, it need to do some work that others won't:
        5.1. Load data for tweets coordinates information
        5.2. Scatter part of the tweets coordinates to the other and the number of the tweets in that part
        5.3. Parallel calculating the tweets coordinates.
        5.4. Master node gather the statistic results from all nodes
        5.5. Order the grid box by 3 different ways:
            5.5.1. Order the Grid Boxes based on the total number of tweets
            5.5.2. Order the rows based on the total number of tweets
            5.5.3. Order the columns based on the total number of tweets
''' 
'''
    Do 5.1.as above:
    
    Note: There is a little tricky here, can't load the whole file since it will exceed the memory
    So we need load the file's specific 'coordinates' part and store it.
''' 
if comm_rank == 0:
    coordiP = []     
    for line in f2:
        if line == "[\n" or line == "]\n":
            continue
        elif line.endswith(',\n'):
            line = line.replace(line,line[0:len(line)-2])
        elif line.endswith('\n'):
            line = line.replace(line,line[0:len(line)-1]) 
        data = json.loads(line)
        coordiP.append(data['json']['coordinates']['coordinates'])
    f2.close()
    
    partitions = [[] for _ in range(comm_size)]
    for i, value in enumerate(coordiP):
        partitions[i%comm_size].append(value)
else:
    partitions = None

'''
    Do 5.2. as above:
    Initiate an empty array for scattering the tweets coordinates information from rank0 node.
'''
localCoordiPs = comm.scatter( partitions, root = 0)  

'''
    Do 5.3. as above:
    Each node assigns tweets coordinates information to their cores equally and automatically.
    and count the total local tweets for each grid box
    
    Note: "localcount" as below is a counter for the total number of tweets 
    that is not in each of the grid box. For testing if there are some tweets
    are in the boundary line of the grid boxes.
'''
localcount = 0
localCountTweet = [ 0 for i in range(num_of_gridBox) ]
for localCoordiP in localCoordiPs:
    flag = 0
    for i in range(num_of_gridBox):
        if  coordi[i][0] <= localCoordiP[0] <= coordi[i][1] and coordi[i][2] <= localCoordiP[1] <= coordi[i][3]:
                localCountTweet[ i ] += 1
                flag = 1
                break
    if flag == 0:
        localcount += 1

'''
    Do 5.4. as above:
    Initiate an empty array for gathering the tweets coordinates information from rank0 node.
'''
countTweet = comm.gather( localCountTweet, root=0)


'''
    Do 5.5. as above:
    Only master node need to order the grid box.
'''
if comm_rank == 0:
    
    # Accumulate the value from different node
    countTweet = list(map(sum,zip(*countTweet)))
    print sum(countTweet)
    '''
        This part is just modifying "countTweet" array, easier to count the total for 5.5.1/5.5.2/5.5.3
        For example:
            countTweet[0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15] like this way, 16 position for the number of tweets in 16 grid boxes
             0->A1, 1->A2, 2->A3, 3->A4, gridA[0,1,2,3]
             4->B1, 5->B2, 6->B3, 7->B4, gridB[4,5,6,7]
             8->C1, 9->C2,10->C3,11->C4,12->C5, gridC[8,9,10,11,12]
            13->D3,14->D4,15->D5, gridD[13,14,15]
            
            Since gridA, gridB, gridC and gridD has different column, modify them for the same column
            So, gridA->[0,1,2,3,0], gridB->[4,5,6,7,0], gridC->[8,9,10,11,12], gridD->[0,0,13,14,15]
            and grid -> [ gridA -> [ [ 0, 1, 2, 3, 0]
                          gridB      [ 4, 5, 6, 7, 0]
                          gridC      [ 8, 9,10,11,12]
                          gridD ]    [ 0, 0,13,14,15] ]
    '''
    gridA = countTweet[0:4]
    gridA.append(0)
    
    gridB = countTweet[4:8]
    gridB.append(0)
    
    gridC = countTweet[8:13]
    
    gridD = countTweet[13:16]
    gridD.insert(0, 0)
    gridD.insert(0, 0)
    
    grid = []
    grid.append( gridA )
    grid.append( gridB )
    grid.append( gridC )
    grid.append( gridD )
    
    # Do the 5.5.1 as above:
    print ("Order the Grid boxes based on the total number of tweets: ")
    print("-----------------------------------------------------------")
    visit = [[0 for col in range(5)] for row in range(4)]
    for k in range( num_of_gridBox ):  
        max = -1
        maxIndexX = maxIndexY = -1
        for i in range(4): 
            for j in range(5):
                if (i == 0 and j == 4) or (i == 1 and j == 4) or (i == 3 and j == 0) or (i == 3 and j == 1):
                    continue
                if grid[i][j] > max and visit[i][j] == 0: 
                    max = grid[i][j]
                    maxIndexX = i
                    maxIndexY = j 
        visit[ maxIndexX ][ maxIndexY ] = 1
        print ("%c%d: %d tweets," %(chr(maxIndexX+65), maxIndexY+1, grid[maxIndexX][maxIndexY] ))
        
    # Do the 5.5.2 as above:
    print ("\nOrder the row based on the total number of tweets: ")
    print("------------------------------------------------------")
    x = list(map(sum,grid))
    visit = [ 0 for col in range(4)]
    for i in range(4):
        max = -1
        maxIndex = -1
        for j in range(4):
            if x[j] > max and visit[j] == 0:
                max = x[j]
                maxIndex = j
        visit[ maxIndex ] = 1
        print ("%c-Row: %d tweets," %(chr(maxIndex+65), x[maxIndex]))
      
    # Do the 5.5.3 as above:
    print ("\nOrder the column based on the total number of tweets: ")
    print("---------------------------------------------------------")
    y = list(map(sum,zip(*grid)))
    visit = [0 for row in range(5)]
    for i in range(5):
        max = -1
        maxIndex = -1
        for j in range(5):
            if y[j] > max and visit[j] == 0:
                max = y[j]
                maxIndex = j
        visit[ maxIndex ] = 1
        print ("Column %d: %d tweets," %( maxIndex+1, y[maxIndex]))

    endtime = time.time()
    print ("Executing time: %.6f" %(endtime-starttime))
