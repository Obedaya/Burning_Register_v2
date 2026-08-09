<template>
  <div class="keypad-wrapper">
    <v-row dense class="mb-2">
      <v-col cols="4" v-for="d in digits" :key="d">
        <v-btn
          block
          size="large"
          variant="outlined"
          @click="keyboardValue(d)"
          class="keypad-btn"
        >
          {{ d }}
        </v-btn>
      </v-col>
      <v-col cols="4">
        <v-btn
          block
          size="large"
          variant="outlined"
          @click="keyboardValue('delete')"
          class="keypad-btn"
        >
          <v-icon>mdi-backspace-outline</v-icon>
        </v-btn>
      </v-col>
    </v-row>

    <v-row dense class="mb-2">
      <v-col cols="4">
        <v-btn
          block
          size="large"
          variant="flat"
          color="error"
          @click="deleteFromCart()"
          class="action-btn"
        >
          <v-icon start>mdi-delete-outline</v-icon>
          Remove
        </v-btn>
      </v-col>
      <v-col cols="4">
        <v-btn
          block
          size="large"
          variant="outlined"
          @click="decreaseProductAmount()"
          class="action-btn"
        >
          <v-icon>mdi-minus</v-icon>
        </v-btn>
      </v-col>
      <v-col cols="4">
        <v-btn
          block
          size="large"
          variant="outlined"
          @click="increaseProductAmount()"
          class="action-btn"
        >
          <v-icon>mdi-plus</v-icon>
        </v-btn>
      </v-col>
    </v-row>

    <v-row dense>
      <v-col cols="4">
        <v-btn
          block
          size="large"
          :color="isTeamActive ? 'success' : undefined"
          :variant="isTeamActive ? 'flat' : 'outlined'"
          @click="toggleTeam()"
          class="action-btn"
        >
          <v-icon start>mdi-account-group</v-icon>
          Team
        </v-btn>
      </v-col>
      <v-col cols="4">
        <v-btn
          block
          size="large"
          variant="flat"
          color="warning"
          @click="clearCart()"
          class="action-btn"
        >
          <v-icon start>mdi-cart-remove</v-icon>
          Clear
        </v-btn>
      </v-col>
      <v-col cols="4">
        <v-btn
          block
          size="large"
          color="primary"
          variant="flat"
          @click="changeView()"
          class="action-btn"
        >
          <v-icon start>mdi-cash-register</v-icon>
          Pay
        </v-btn>
      </v-col>
    </v-row>
  </div>
</template>

<script>
export default {
  data() {
    return {
      digits: ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "00"],
    };
  },
  props: {
    isTeamActive: {
      type: Boolean,
      default: false,
    },
  },
  methods: {
    keyboardValue(d) {
      this.$emit("keyboard", d);
    },
    clearCart() {
      this.$emit("clearCart");
    },
    toggleTeam() {
      this.$emit("toggleTeam");
    },
    changeView() {
      this.$emit("changeView");
    },
    deleteFromCart() {
      this.$emit("deleteFromCart");
    },
    increaseProductAmount() {
      this.$emit("increaseProductAmount");
    },
    decreaseProductAmount() {
      this.$emit("decreaseProductAmount");
    },
  },
};
</script>

<style scoped>
.keypad-btn {
  font-size: 1.1rem;
  font-weight: 600;
  min-height: 48px;
  text-transform: none;
  letter-spacing: 0;
  border-color: rgba(255, 255, 255, 0.2) !important;
  color: #EAEAEA !important;
}
.keypad-btn:hover {
  border-color: rgba(255, 107, 107, 0.5) !important;
  background: rgba(255, 255, 255, 0.05);
}
.action-btn {
  text-transform: none;
  letter-spacing: 0;
  min-height: 48px;
}
</style>
