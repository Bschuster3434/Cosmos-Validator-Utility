import boto3
import subprocess
import time

def main():
    #Find all the VotingPeriod Votes
    #If None, sleep for a few seconds

    subprocess.check_output(['gaiacli', 'gov', 'query-proposals', '--status', 'VotingPeriod'])
