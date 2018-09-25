<template>
  <div id="app">
    <div class="container">
      <app-header></app-header>
      <app-validator-choice
      @updateSelectedValidator="selectedValidator = $event.validator"
      :validatorVotes="validatorVotes"></app-validator-choice>
          <app-voting-record
          :selectedValidator="selectedValidator"
          :govResults="govResults"
          :validatorVotes="validatorVotes"
          v-if="validatorVotes != null"></app-voting-record>
          <app-email-alert></app-email-alert>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import ActiveVotes from './components/gov/ActiveVotes.vue'
import VotingRecord from './components/gov/VotingRecord.vue'
import Header from './components/shared/Header.vue'
import Footer from './components/shared/Footer.vue'
import ValidatorChoice from './components/validators/ValidatorChoice.vue'
import EmailAlert from './components/email/EmailAlert.vue'
import axios from 'axios'


export default {
  mounted: function() {
    axios
      .get('https://4itjqoal2g.execute-api.us-east-1.amazonaws.com/dev/gov/results')
      .then(response => (this.govResults = response.data))
      .catch(error => console.log(error))
  },
  data : function () {
    return {
      selectedValidator : "",
      govResults : null,
      validatorVotes : null,
    }
  },
  components: {
      'app-header': Header,
      'app-footer': Footer,
      'app-validator-choice': ValidatorChoice,
      'app-active-votes': ActiveVotes,
      'app-voting-record': VotingRecord,
      'app-email-alert' : EmailAlert,
    },
  watch: {
    selectedValidator : function() {
      axios
        .get('https://4itjqoal2g.execute-api.us-east-1.amazonaws.com/dev/gov/validatorvotes/' + this.selectedValidator.validatorKey.S)
        .then(response => (this.validatorVotes = response.data))
    }
  }
}
</script>

<style>

</style>
