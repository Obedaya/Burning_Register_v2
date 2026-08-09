<template>
  <div class="button-panel">
    <div class="categories-row mb-3">
      <v-btn
        v-for="(cat, i) in getAllCategories(products, 'category')"
        :key="i"
        :color="selectedCategory === cat ? 'primary' : 'surface-bright'"
        @click="selectCategory(products, 'category', cat)"
        size="large"
        class="category-btn mr-2"
        :variant="selectedCategory === cat ? 'flat' : 'tonal'"
      >
        <v-icon start>{{ getCategoryIcon(cat) }}</v-icon>
        {{ cat }}
      </v-btn>
    </div>

    <v-row dense>
      <v-col
        cols="6" sm="4" md="3"
        v-for="(item, i) in selectedItems"
        :key="i"
      >
        <v-card
          @click="addItem(item)"
          class="product-card pa-3 d-flex flex-column align-center justify-center"
          :color="'surface-bright'"
          hover
          height="90"
        >
          <div class="text-body-1 font-weight-medium text-center">{{ item.name }}</div>
          <div class="text-caption text-medium-emphasis mt-1">{{ formatPrice(item.price) }}</div>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script>
export default {
  data() {
    return {
      selectedItems: [],
      selectedCategory: null,
    };
  },
  props: {
    products: {
      type: Array,
      default: () => [],
    },
    visible: {
      type: Boolean,
      default: true,
    },
  },
  watch: {
    products: {
      handler(newProducts) {
        if (newProducts.length > 0 && !this.selectedCategory) {
          const categories = this.getAllCategories(newProducts, 'category');
          if (categories.length > 0) {
            this.selectedCategory = categories[0];
            this.selectCategory(newProducts, 'category', categories[0]);
          }
        }
      },
      immediate: true,
    },
  },
  methods: {
    addItem(item) {
      this.$emit("addItem", item);
    },
    selectCategory(list, key, value) {
      this.selectedCategory = value;
      this.selectedItems = list.filter((item) => item[key] === value);
    },
    getAllCategories(list, categoryKey) {
      const categories = new Set();
      list.forEach((item) => {
        if (Object.prototype.hasOwnProperty.call(item, categoryKey)) {
          categories.add(item[categoryKey]);
        }
      });
      return Array.from(categories);
    },
    getCategoryIcon(category) {
      const icons = {
        'Drinks': 'mdi-cup',
        'Snacks': 'mdi-food-croissant',
        'Sweets': 'mdi-candy',
        'Tickets': 'mdi-ticket',
        'Pfand': 'mdi-recycle',
      };
      return icons[category] || 'mdi-tag';
    },
    formatPrice(price) {
      return `${parseFloat(price).toFixed(2)}€`;
    },
  },
};
</script>

<style scoped>
.product-card {
  cursor: pointer;
  transition: all 0.15s ease;
  border: 1px solid rgba(255, 255, 255, 0.15);
}
.product-card:hover {
  border-color: rgba(255, 107, 107, 0.5);
  transform: translateY(-1px);
  background-color: rgba(255, 255, 255, 0.05) !important;
}
.category-btn {
  text-transform: none;
  letter-spacing: 0;
}
</style>
