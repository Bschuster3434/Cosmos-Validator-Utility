<template>
  <div>
    <h3>Active Votes</h3>
      <template v-for="vote in govActiveResultsOrdered">
      <p>{{ vote.proposalId.N }} - {{ vote.title.S }}</p>
      <p>Description - {{vote.description.S}}</p>
      <p>Vote Start Block: {{vote.votingStartBlock.N}}</p>
      <p>Validator Current Vote: {{vote.castVoteFor.S}}</p>
      <hr />
      </template>
  </div>
</template>

<script>
import _ from 'lodash';

export default {
  props : [
    'selectedValidator',
    'govResults',
    'validatorVotes'
  ],
  computed : {
    govActiveResultsOrdered : function() {
      let items = this.govResults.Items;
      let activeItems = items.filter((item) => {
        return item.proposalStatus.S == 'VotingPeriod'
      });

      for (var i=0; i < activeItems.length; i++) {
          let nextItem = activeItems[i];
          for (var e=0; e < this.validatorVotes.Items.length; e++) {
            let nextValidatorVote = this.validatorVotes.Items[e];
            if (nextItem.proposalId.N == nextValidatorVote.proposalId.N) {
              activeItems[i]["castVoteFor"] = {
                "S" : nextValidatorVote.castVoteFor.S
              };
              break;
            }
          };
      }
      return _.orderBy(activeItems, 'votingStartBlock.N')
    }
  }
}
</script>

<style>

</style>
