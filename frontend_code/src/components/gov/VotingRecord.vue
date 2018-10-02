<template>
  <div class="panel-group">
    <div class="panel panel-default">
      <div class="panel-heading">
        <h3>Finished Votes</h3>
        <p>Click on the row for details of each vote</p>
      </div>
        <div class="panel-body">
        <table class="table">
          <thead>
            <tr>
              <th scope="col">ID #</th>
              <th scope="col">Proposal Title</th>
              <th scope="col">Proposal Details</th>
              <th scope="col">Proposal Status</th>
              <th scope="col">Validator Vote</th>
            </tr>
          </thead>
          <tbody>
            <template v-for="result in govAllResultsOrdered.slice(this.resultPaginationStart,this.resultPaginationStart + 10)">
              <tr @click="showVoteDetails(result.proposalId.N)">
                <td scope="row">{{result.proposalId.N}}</td>
                <td>{{result.title.S}}</td>
                <td>{{result.description.S.substring(0,70)}}</td>
                <td v-if="result.proposalStatus.S == 'Passed'">
                    <p :style="{'color' : 'green'}">{{result.proposalStatus.S}}</p>
                  </td>
                  <td v-else-if="result.proposalStatus.S == 'Rejected'">
                    <p :style="{'color' : 'red'}">{{result.proposalStatus.S}}</p>
                  </td>
                  <td v-else>
                    <p :style="{'color' : 'orange'}">{{result.proposalStatus.S}}</p>
                  </td>
                <td v-if="result.castVoteFor.S == 'No Result Found'">No Result Found</td>
                  <td v-else-if="result.castVoteFor.S == 'Validator Offline'">
                    <p><strong>{{result.castVoteFor.S}}</strong></p></td>
                  <td v-else-if="result.castVoteFor.S == 'Yes'">
                    <p :style="{'color' : 'green'}">{{result.castVoteFor.S}}</p></td>
                  <td v-else-if="result.castVoteFor.S == 'No' |  result.castVoteFor.S == 'NoWithVeto'">
                    <p :style="{'color' : 'red'}">{{result.castVoteFor.S}}</p></td>
                  <td v-else-if="result.castVoteFor.S == 'Void'">
                    <p :style="{'color' : 'red'}"><strong>{{result.castVoteFor.S}}</strong></p></td>
                  <td v-else>
                    <p>{{result.castVoteFor.S}}</p></td>
              </tr>
              <tr  v-if="showDetailByProposalId == result.proposalId.N">
                <td colspan="12">
                  <div v-if="'castVoteFor' in result" class="col-sm-6">
                    <h4>#{{result.proposalId.N}} : {{result.title.S}}</h4>
                    <p>Proposal Status: {{result.proposalStatus.S}} / Validator Vote: {{result.castVoteFor.S}}</p>
                    <p>Full Description: {{result.description.S}}</p>
                    <p>Submitted On Block: {{result.votingStartBlock.N}}</p>
                  </div>
                  <div v-else class="col-sm-6">
                    <h4>#{{result.proposalId.N}} : {{result.title.S}}</h4>
                    <p>Proposal Status: {{result.proposalStatus.S}} / Validator Vote: No Result Recorded</p>
                    <p>Full Description: {{result.description.S}}</p>
                  </div>
                  <div class="col-sm-6">
                    <h4>Vote Breakout</h4>
                    <p>Yes Votes:       {{result.voted_yes.S}}</p>
                    <p>No Votes:        {{result.voted_no.S}}</p>
                    <p>Voted No with Veto: {{result.voted_no_with_veto.S}}</p>
                  </div>
                </td>
              </tr>
            </template>
          </tbody>
        </table>
        <div class="container-fluid">
          <div class="row">
            <div class="col-md-9"></div>
            <div class="col-md-3 txt-right">
              <button class="btn btn-primary" @click="paginateResultsBackwards">Previous Results</button>
              <button class="btn btn-primary" @click="paginateResultsForward">Next Results</button>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data : function() {
    return {
      resultPaginationStart : 0,
      showDetailByProposalId : null,
    }
  },
  props : [
    'selectedValidator',
    'govResults',
    'validatorVotes'
  ],
  methods : {
    paginateResultsForward : function () {
      if (this.resultPaginationStart + 10 >= this.govAllResultsOrdered.length) {
        this.resultPaginationStart += 0;
      }
      else {
        this.resultPaginationStart += 10;
      }
    },
    paginateResultsBackwards : function () {
      if (this.resultPaginationStart >= 10) {
        this.resultPaginationStart -= 10;
      }
      else {
        this.resultPaginationStart = 0;
      }
    },
    showVoteDetails : function (proposalId) {
      if (this.showDetailByProposalId == proposalId) {
        this.showDetailByProposalId = null;
      }
      else {
        this.showDetailByProposalId = proposalId;
      }
    },
  },
  computed : {
    govAllResultsOrdered : function() {
      //let items = this.govResults.Items;
      //let activeItems = items.filter((item) => {
        //return item.proposalStatus.S != 'VotingPeriod'
      //});

      let activeItems = this.govResults.Items;


      for (var i=0; i < activeItems.length; i++) {
          if (parseInt(activeItems[i].proposalId.N) > 540) {
            activeItems[i]["castVoteFor"] = {};
            activeItems[i]["castVoteFor"].S = "Validator Offline"
          }
          else {
            activeItems[i]["castVoteFor"] = {};
            activeItems[i]["castVoteFor"].S = "No Result Found";
          }
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
      return _.orderBy(activeItems, ['votingStartBlock.N'], ['desc'])
    }
  },
}
</script>

<style>

</style>
