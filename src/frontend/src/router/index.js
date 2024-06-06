import { createWebHistory, createWebHashHistory, createRouter } from "vue-router";
import Home from "@/views/Home.vue";
import Search from "@/views/Search.vue";
import Chat from "@/views/Chat.vue";
import About from "@/views/About.vue";
import Gemeente from "@/views/Gemeente.vue";
import GemeenteType from "@/views/GemeenteType.vue";
import GemeenteYear from "@/views/GemeenteYear.vue";
import Video from "@/views/Video.vue";

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
  },
  {
    path: "/search",
    name: "Search",
    component: Search,
  },
  {
    path: "/chat",
    name: "Chat",
    component: Chat,
  },
  {
    path: "/about",
    name: "About",
    component: About,
  },
  {
    path: "/gemeente/:gemeenteName",
    name: "Gemeente",
    component: Gemeente,
    props: true,
  },
  {
    path: "/gemeente/:gemeenteName/:gemeenteType",
    name: "GemeenteType",
    component: GemeenteType,
    props: true,
  },
  {
    path: "/gemeente/:gemeenteName/:gemeenteType/:gemeenteYear",
    name: "GemeenteYear",
    component: GemeenteYear,
    props: true,
  },
  {
    path: "/gemeente/:gemeenteName/:gemeenteType/:gemeenteYear/:videoID",
    name: "Video",
    component: Video,
    props: true,
  },
];

const router = createRouter({
  history: createWebHashHistory(),
  routes,
});

export default router;
