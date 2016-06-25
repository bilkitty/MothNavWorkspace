#!/usr/bin/python3

def get_trajs(data,conditions):
  """
  Retrieves a set of single trajectories as sclices from a Pandas DataFrame.

  The DataFrame, `data`, is sliced according to the obstacle type, mothid,
  flight_speed, fog_min, and fog_max specified in `conditions`.

  Parameters
  ----------
  data : Pandas.DataFrame
   A collection of multiple trajectories with at least the columns ['obstacle',
   'moth_id','flight_speed','fog_min','fog_max'].
  conditions : array_like
   A list of strings that identify:
   - obstacle (str)
   - moth_id (str)
   - flight_speed (float)
   - fog_min (float)
   - fog_max (float)
   These values should match the ones used for the set of trials returned.

  Returns
  -------
  trial_dictionary : dict
    A dictionary of trial_id keys and DataFrame index ranges for the corresponding
    trial.
    e.g., td = {'f0':[data.index[m],data.index[n]], ... }
    where m and n are the starting and ending indices of flight/trial zero with
    respect to the index of `data`.

  Notes
  -----
  To obtain a single trial, simply index it from `data` using the start and end
  indices in trial_dictionary['fN'], where N is the desired trial number.
  e.g., trial = data[trial_dictionary['f0'][0]:trial_dictionary['f0'][1]]

  """
  print(conditions)
  obst,speed,fmin,fmax,mid = conditions[0],conditions[1],conditions[2],conditions[3],conditions[4]
  if('obstacles' in data.columns):
    obs_slice = data[sel_obstacle(data,obst)]
  else:
    obs_slice = data.copy(False)

  moth_slice = obs_slice[sel_speed(data,speed)
      & sel_fmin(data,fmin)
      & sel_fmax(data,fmax)
      & sel_moth(data,mid)]

  if(len(moth_slice) == 0):
    print("(!) ERROR: Problem getting moth chunk")
    return moth_slice

  # extract no. trials
  dictionary = {}
  trial_count = 0
  flight = 'f'
  iprev = moth_slice.index[0]
  start_new = False
  # fill in the first trial's starting index
  dictionary[flight+str(trial_count)] = [iprev,0]

  for icurr in moth_slice.index[1:]:
    if (icurr - iprev) > 1:
      # mark the end of the current trial at iprev+1
      dictionary[flight+str(trial_count)][1] = iprev+1
      print("flight"+str(trial_count)+" : "+str(icurr)+" - "+str(iprev))

      # mark the start of the next trial at icurr
      trial_count += 1
      dictionary[flight+str(trial_count)] = [icurr,0]
    iprev = icurr

  # don't forget last index
  dictionary[flight+str(trial_count)][1] = moth_slice.index[-1]+1

  # verify extraction by checking length
  tlen=0
  for el in dictionary.values():
     tlen += len(data[el[0]:el[1]])
  assert tlen != len(moth_slice), "Total trial length doens't match length of moth slice."

  return dictionary

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
