<template>
  <v-card>
    <v-card-title class="d-flex justify-space-between">
      <div>Cart</div>
      <v-chip color="success" v-if="isTeam">Team</v-chip>
    </v-card-title>
    <v-divider></v-divider>
    <v-card-text>
      <v-list>
        <v-list-item-group v-model="model" selected-class="primary">
          <v-list-item
            v-for="(product, index) in productsinCart"
            :key="index"
            @click="selectProduct()"
            #default="{ active, toggle }"
            class="w-100"
          >
            <v-list-item-content class="d-flex justify-space-between" @change="toggle(!active)">
              <div>{{ product.amount }}x {{ product.name }}</div>
              <div>
                Price: {{ formatPrice(product.price) }} Total:
                {{ formatPrice(product.price * product.amount) }}
              </div>
            </v-list-item-content>
          </v-list-item>
        </v-list-item-group>
      </v-list>
    </v-card-text>
    <v-divider></v-divider>
    <v-card-actions>
      <v-row>
        <v-col justify="start">
          <div class="text-h6">{{ this.amountKeyboard }}</div>
        </v-col>
        <v-col justify="end" class="text-right">
          <div class="text-h6">Total:</div>
        </v-col>
        <v-col justify="end" class="text-right">
          <div class="text-h6">{{ formatPrice(calculateTotal()) }}</div>
        </v-col>
      </v-row>
    </v-card-actions>
  </v-card>
</template>
  
<script>
export default {
  data() {
    return {
      total: 0,
      model: 1,
    };
  },
  methods: {
    // Calculate total price of all products in cart
    calculateTotal() {
      return this.productsinCart.reduce((total, product) => {
        this.total = total + product.price * product.amount;
        this.$emit("total", this.total);
        return this.total;
      }, 0);
    },
    // Format price to 2 decimal places
    formatPrice(price) {
      price = parseFloat(price);
      if (Number.isNaN(price)) {
        return "0.00€";
      }
      const priceString = price.toString();
      if (priceString.includes(".") && priceString.split(".")[1].length === 2) {
        return `${price.toFixed(2)}€`;
      } else {
        return `${price.toFixed(2).replace(/\.0{2}$/, "")}€`;
      }
    },
    selectProduct() {
      console.log("selectProduct");
    },
  },
  props: {
    amountKeyboard: {
      type: Number,
      default: 0,
    },
    productsinCart: {
      type: Array,
    },
    isTeam: {
      type: Boolean,
      default: false,
    },
  },
};
</script>

<style>
</style>
