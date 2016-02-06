#!/usr/bin/python3

# returns dictionary of trajectories by start and end indices
# key = 't'+n, value = [range1,range2]
def get_trajs(data,obst,speed,fmin,fmax,mid):
   if('obstacles' in data.columns):
      obs_slice = data[sel_obstacle(data,obst)]
   else:
      obs_slice = data.copy(False)

   moth_slice = obs_slice[sel_speed(data,speed)
         & sel_fmin(data,fmin)
         & sel_fmax(data,fmax)
         & sel_moth(data,mid)]

   # extract no. trials
   dd = {}
   iit = 0
   flight = 'f'
   iprev = moth_slice.index[0]
   start_new = False
   dd[flight+str(iit)] = [iprev,0]

   # save icurr as start of next trial and
   # 1 after iprev as end of last trial
   for ii in moth_slice.index[1:]:
      if (ii - iprev) > 1:
         dd[flight+str(iit)][1] = iprev+1
         print("flight"+str(iit)+" : "+str(ii)+" - "+str(iprev))
         iit += 1
         dd[flight+str(iit)] = [ii,0]
      iprev = ii

   # don't forget last index
   dd[flight+str(iit)][1] = moth_slice.index[-1]+1

   #--DEBUG
   # verify extraction by checking length
   tlen=0
   for el in dd.values():
       tlen += len(data[el[0]:el[1]])

   if(tlen != len(moth_slice)):
      print("tlen: "+str(tlen))
      print("ms: "+str(len(moth_slice)))
      print("failed to obtain trajs")

   return dd

def sel_moth(block,name):
   return block.moth_id == name

def sel_obstacle(block,name):
   return block.obstacles == name

def sel_speed(block,val):
   return block.flight_speed == val

def sel_fmin(block,val):
   return block.fog_min == val

def sel_fmax(block,val):
   return block.fog_max == val
