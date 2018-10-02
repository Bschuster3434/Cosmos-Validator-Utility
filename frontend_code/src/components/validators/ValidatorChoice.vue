<template>
<div class="panel-group">
  <div class="panel panel-default">
    <div class="panel-heading"><h4>Choose Validator (From Active Validators)</h4></div>
    <div class="panel-body">
      <select v-model="selectedValidator">
        <option disabled value="">Please select a validator</option>
        <template v-for="(nextValidator, index) in validators" v-if="nextValidator.revoked.BOOL == false" >
          <option v-bind:value="nextValidator">{{nextValidator.moniker.S}} | {{nextValidator.validatorKey.S}}</option>
        </template>
      </select>
    </div>
  </div>
  <div class="panel panel-default" v-if="selectedValidator != '' & validatorVotes != null">
    <div class="panel-heading">
      <h4><strong>{{selectedValidator.moniker.S}}</strong>: Validator Details</h4>
      <div v-if="!selectedValidator.hasOwnProperty('website')">
        <p>No Validator Website</p>
      </div>
      <div v-else-if="selectedValidator.website.S == '[do-not-modify]'">
        <p>No Validator Website</p>
      </div>
      <div v-else>
        <a :href="selectedValidator.website.S">Validator Website</a>
      </div>
    </div>
    <div class="panel-body">
      <div class="container">
        <div class="row">
          <div class="col-sm-6">
            <p>Validator Key: {{selectedValidator.validatorKey.S}}</p>
            <p>Public Key: {{selectedValidator.pub_key.S}} </p>
            <p>Public Key Type: {{selectedValidator.pub_key_type.S}}</p>
          </div>
          <div class="col-sm-6">
            <p>Bond Height: {{selectedValidator.bond_height.S}}</p>
            <p>Tokens: {{selectedValidator.tokens.S}}</p>
            <div v-if="participatingVotes.castVotes == participatingVotes.totalVotes">
              <p :style="{'color' : 'green'}">Voting Rate: {{participatingVotes.castVotes}}/{{participatingVotes.totalVotes}}</p>
            </div>
            <div v-else>
              <p :style="{'color' : 'red'}">Voting Rate: {{participatingVotes.castVotes}}/{{participatingVotes.totalVotes}}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</div>
</template>

<script>
import axios from 'axios'

export default {
  mounted: function() {
    axios
      .get('https://4itjqoal2g.execute-api.us-east-1.amazonaws.com/dev/validators/getallvalidators')
      //.then(response => (this.validators = response.data))
      .then(response => this.validators = _.orderBy(response.data.Items, ['moniker.S'], ['asc']))
      .catch(error => console.log(error))
  },
  props : ['validatorVotes'],
  data : function() {
    return {
      validators : null,
      selectedValidator: ""
    }
  },
  watch: {
    selectedValidator: function () {
      this.$emit('updateSelectedValidator', {
        validator : this.selectedValidator
      });
    }
  },
  computed: {
    participatingVotes: function() {
      let resp_obj = {};
      let items = this.validatorVotes.Items;

      resp_obj.totalVotes = items.length;

      let castVotes = 0;

      for (var i = 0; i < items.length; i++) {
        if (items[i].castVoteFor.S != 'Void') {
          castVotes++;
        }
      };

      resp_obj.castVotes = castVotes;

      return resp_obj

    },
    orderedValidators: function() {
      return _.orderBy(this.validators.Items, ['moniker.S'], ['asc'])
    },
  }
}

</script>

<style>

</style>
