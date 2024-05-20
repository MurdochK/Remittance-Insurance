<template>
  <div>
    <h1>Car Insurance Policy</h1>
    <div v-if="policy">
      <p>Policy ID: {{ policy.policyId }}</p>
      <p>Insured: {{ formatAddress(policy.insured) }}</p>
      <p>Age: {{ policy.age }}</p>
      <p>Premium Amount: {{ policy.premiumAmount }}</p>
      <p>Average Speed: {{ policy.averageSpeed }} km/hr</p>
      <p>Driving Location: {{ policy.drivingLocation }}</p>
      <p>Has Telematics: {{ policy.hasTelematics }}</p>
      <p>Drinking History: {{ policy.drinkingHistory }}</p>
      <p>Health Status: {{ policy.healthStatus }}</p>
      <p>Occupation: {{ policy.isActuary ? 'Actuary' : 'Other' }}</p>
      <div v-if="policy.imageHash">
        <h3>Policy Image</h3>
        <img :src="getImageUrl(policy.imageHash)" alt="Policy Image" />
      </div>
    </div>
    <div v-else>
      <p>Loading policy details...</p>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      policy: null,
    };
  },
  mounted() {
    this.fetchPolicyDetails();
  },
  methods: {
    async fetchPolicyDetails() {
      try {
        const policyId = 1; // Replace with the actual policy ID
        const response = await fetch(`/api/policies/${policyId}`);
        this.policy = await response.json();
      } catch (error) {
        console.error('Error fetching policy details:', error);
      }
    },
    formatAddress(address) {
      // Implement a function to format the address for anonymity
      return '0x' + address.slice(0, 6) + '...' + address.slice(-4);
    },
    getImageUrl(imageHash) {
      // Implement a function to retrieve the image URL based on the image hash
      return `https://example.com/images/${imageHash}`;
    },
  },
};
</script>
