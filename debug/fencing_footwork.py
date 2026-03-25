import pyttsx3
import argparse
import time
import random 
from datetime import datetime

def read_lesson(file_path):
	# Initialize the TTS engine
	engine = pyttsx3.init()
	voices = engine.getProperty('voices')
	#engine.setProperty('voice', voices[64].id)
	#engine.setProperty('rate', 125)
	try:
		# Open and read the text file
		with open(file_path, 'r', encoding='utf-8') as file:
			content = file.readlines()

		for line in content:
			line_splt = line.split()
			if len(line_splt) == 0: continue
			if line_splt[0] == "pause":
				engine.runAndWait()
				time.sleep(float(line_splt[1]))
			else:
				print("saying %s"%line.strip())
				engine.say(line.strip())
		engine.runAndWait()

	except FileNotFoundError:
		print(f"Error: The file at {file_path} was not found.")
	except Exception as e:
		print(f"An error occurred: {e}")


# returns the advance length, retreat length, long retreat length, and lunge lengths 
# for different fencer classes in feet

def get_fencer_pars(fencerType,settings):
	if fencerType == "child":
			 # adv.  ret.  long-ret. lunge  double-adv. double-ret.  adv-lunge  retr-lunge   long-lunge   fleche  redouble  duck
		return [0.7,  -0.7,   -1.3,    0.0,      1.5,       -1.5,        2.0,        -0.75,       2.0,       4,   3.0,     0.0]
	elif fencerType == "normal":
		return [1.0, -1.0, -1.6, 0.0, 2.0, -2.0, 3.8, -1.1, 2.5, 7.0, 5.0, 0.0]
	elif fencerType == "athletic":
		return [1.2, -1.2, -1.9, 0.0, 2.4, -2.4, 4.5, -1.3, 3.0, 8.0, 6.0, 0.0]
	elif fencerType == "custom":
		return [1.2, -1.2, -1.9, 0.0, 2.4, -2.4, 4.5, -1.3, 3.0, 8.0, 6.0, 0.0]
	else:
		raise ValueError("ERROR: Incorrect fencer type: %s"%fencerType)


# return the tempi (= time to complete) for each different action (advance, retreat, long retreat, lunge) in seconds
def get_action_tempi(pace):
	if pace == 1:
			   # advance  retreat  long-retreat   lunge  double-adv double-ret adv-lunge retr-lunge long-lunge   fleche    redouble     duck
		return     [3.0,     3.0,       3.0,        5.0,     4.0,       4.0,        6.,        6.,       5.,        8.,       6.0,       4.0]
	elif pace == 2:
		return     [2.2,     2.2,       2.2,        3.0,     3.0,       3.0,        3.5,       3.5,      3.5,       6.0,      4.4,       3.2]
	elif pace == 3:
		return     [1.8,     1.8,       1.8,        2.2,     2.5,       2.5,        2.7,       2.7,      3.0,       5.5,      4.0,       2.7]
	elif pace == 4:
		return     [1.25,     1.25,     1.25,       2.1,     2.2,       2.2,        2.5,       2.4,      2.3,       5.5,       3.3,      2.3]
	elif pace == 5: 
		return     [1.0,     1.0,       1.2,        1.9,     1.8,       1.8,        2.3,       2.15,     2.1,       5.0,       3.0,      2.0]

# return the action frequency (= probability of certain actions). Advance = 0, retreat = 1, long retreat = 2, lunge = 3, etc.
def get_rand_action(complexity,pos,piste_length):
		# augment the probabilities with forward/backward penalties if the position is too close to one side
		#penalty = 
		rand_action = random.random()
		if complexity == 1:
					    #  adv.  ret  long_ret  lung    # 1 forward action, 1 backwards action, 1 neutral
			actions_fs = [0.4,  0.35,  0.10,   0.15]
		elif complexity == 2:
					    #  adv.  ret  long_ret  lung   double-adv. double-ret adv_lunge  retr_lunge long_lunge  # 4 forward actions, 4 backwards actions, 1 neutral
			actions_fs = [0.20,  0.20,  0.05,   0.10,      0.10,       0.10,     0.10,      0.05,     0.10]
		elif complexity == 3:
					    #  adv.  ret    long_ret  lung   double-adv.  double-ret. adv_lunge  retr_lunge long_lunge flech   redouble   duck       6 forward actions, 4 backwards, 2 neutral
			actions_fs = [0.15,  0.225,  0.05,    0.10,     0.075,       0.15,      0.075,      0.05,     0.05,     0.025,   0.025,   0.025]
		actions_int = [0 for iii in range(len(actions_fs)+1)]
		
		if sum(actions_fs) > 1.0: 
			raise ValueError("ERROR: sum of action frequencies is greater than 1.0: %s"%(sum(actions_fs)))

		for iii in range(1,len(actions_fs)+1): 
			actions_int[iii] = actions_fs[iii-1] + actions_int[iii-1]

			if rand_action > actions_int[iii-1] and rand_action < actions_int[iii]:
				return iii - 1

		raise ValueError("ERROR: random action not identified!")
		return
 
def isValidAction(action_len, pos, piste_length, end_margin):
	# does this put the 
	if ( (pos + action_len) < (piste_length - end_margin) and (pos + action_len) > (end_margin) ): return True
	else: return False


def create_lesson(fencerType, time_left, pace, piste_length, end_margin, complexity,  outfile_str):

	action_lens	 = get_fencer_pars(fencerType)
	action_ts    = get_action_tempi(pace)

	pos = piste_length / 2.0

	actions = ["advance", "retreat", "long-retreat", "lunge",  "double-advance", "double-retreat",  "advance-lunge", "retreat-lunge", "long-lunge", "fleche", "redouble", "duck"]


	if complexity == 1:
		num_actions = 4
	elif complexity == 2:
		num_actions = 9
	elif complexity == 3:
		num_actions = 12


	# create the lesson plan text file
	with open("test%s.txt" % outfile_str, "w") as lesson:

		#lesson.write("Hey, kids\n")
		#lesson.write("Welcome to Uncle Scott's torture chamber: %s seconds in hell\n"%(time_left))
		lesson.write("Let's get started in five\n")
		lesson.write("pause 1\n")
		lesson.write("four\n")
		lesson.write("pause 1\n")
		lesson.write("three\n")
		lesson.write("pause 1\n")
		lesson.write("two\n")
		lesson.write("pause 1\n")
		lesson.write("one\n")
		lesson.write("pause 1\n")

		chosen_actions = [0 for iii in range(num_actions)]

		while time_left > 0:
			valid_action = False
			action = None
			while not valid_action:
				# generate a random action
				action 		  = get_rand_action(complexity,pos, piste_length)
				valid_action  = isValidAction(action_lens[action], pos, piste_length, end_margin)
			if action in list(range(num_actions)):
				lesson.write("%s\n"%(actions[action]))
				lesson.write("pause %s\n"%(action_ts[action]))
				chosen_actions[action]+=1
			else:
				raise ValueError("ERROR: no valid action determined.")

			time_left -= action_ts[action]
			pos 	  += action_lens[action]
			if pos < 0 or pos > piste_length:
				raise ValueError("ERROR: fencer position is off the piste.")

		lesson.write("Lesson complete.\n")
		lesson.write("Well done.\n")


		print("Recorded the following actions: ")
		for iii in range(num_actions):
			print("%s : %s"%(actions[iii], chosen_actions[iii]))
	return
	
if __name__=="__main__":

	parser = argparse.ArgumentParser()
	parser.add_argument("--infile", help="Input File path")
	parser.add_argument("--fencerType", required=True, help="Fencer type of the user(s). Options: child, normal, athletic")
	parser.add_argument("--pisteLength", type=int, required=True, help="Length of the piste being used (in feet)")
	parser.add_argument("--duration", type=int, required=False, default = 60, help="Duration of exercise (in seconds)")
	parser.add_argument("--pace", type=int, required=False, default = 2, help="Pace setting that determines speed of actions (1-5, default is 2)")
	parser.add_argument("--endMargin", type=int, required=False, default = 8, help="How far from the start or end of the piste to start moving backwards (in feet).")
	parser.add_argument("--saveExercise", required=False, action='store_true', help="Save the exercise itinerary.")
	parser.add_argument("--complexity", type=int, required=False, default = 3, help="The level of complexity of the actions to include (options: 1-3, default = 3.")


	args = parser.parse_args()

	engine = pyttsx3.init()
	voices = engine.getProperty('voices')

	#for index, voice in enumerate(voices):
	#	print(f"Index: {index} | Name: {voice.name} | Languages: {voice.languages}")

	fencerType = args.fencerType.lower()

	if fencerType not in ["child", "normal", "athletic"]:
		raise ValueError("ERROR: fencerType %s is not one of the accepted options: child, normal, athletic"%(fencerType))
	if args.pace > 5 or args.pace < 1: 
		raise ValueError("ERROR: pace setting %s is not in the acceptable range (1-5)."%args.pace)
	if args.complexity not in [1,2,3]:
		raise ValueError("ERROR: invalid complexity: %s. Valid options are 1 (simple actions), 2 (compound actions), 3 (complex actions) ")


	infile = "test.txt"

	outfile_str = ""
	if args.saveExercise:
		now = datetime.now()
		outfile_str = now.strftime("_%d-%m-%Y %H:%M:%S")
		infile = "test%s.txt"%outfile_str
	if args.infile: infile = args.infile
	else:	create_lesson(fencerType, args.duration,args.pace, args.pisteLength, args.endMargin, args.complexity, outfile_str)


	# create lesson plan for x minutes
	read_lesson(infile)

	### vary the sleep timing




