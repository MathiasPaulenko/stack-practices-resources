<!-- view/UserListView.vue -->
<script setup lang="ts">
import { ref, onMounted } from 'vue';
import { UserController, UserModel } from './userMVC';
import type { User } from './userMVC';

const model = new UserModel();
const controller = new UserController(model);
const users = ref<User[]>([]);
const query = ref('');

onMounted(async () => {
  await controller.loadUsers();
  users.value = controller.search('');
});

const handleSearch = (q: string) => {
  query.value = q;
  users.value = controller.search(q);
};
</script>

<template>
  <div>
    <input
      type="search"
      v-model="query"
      @input="handleSearch(query)"
      placeholder="Search users..."
    />
    <ul>
      <li v-for="u in users" :key="u.id">{{ u.name }} — {{ u.email }}</li>
    </ul>
  </div>
</template>
