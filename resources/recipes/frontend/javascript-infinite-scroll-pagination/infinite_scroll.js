// Infinite scroll on IntersectionObserver: loading/error states,
// AbortController teardown, DocumentFragment batching, a11y roles.
// Works as an ES module in the browser: import { InfiniteScroll } from "./infinite_scroll.js"

export class InfiniteScroll {
    constructor(options) {
        this.container = options.container;
        this.sentinel = options.sentinel;
        this.fetchUrl = options.fetchUrl;
        this.renderItem = options.renderItem;
        this.pageSize = options.pageSize ?? 10;
        this.threshold = options.threshold ?? 200;

        this.page = 1;
        this.loading = false;
        this.hasMore = true;
        this.observer = null;
        this.controller = null;
    }

    init() {
        this.loadInitial();
        this.setupObserver();
    }

    async loadInitial() {
        this.showLoading();
        try {
            const data = await this.fetchPage(1);
            this.renderItems(data.items);
            this.hasMore = data.hasMore;
        } catch (err) {
            this.showError("Failed to load initial data");
        }
        this.hideLoading();
    }

    setupObserver() {
        this.observer = new IntersectionObserver(
            (entries) => this.handleIntersection(entries),
            { rootMargin: `${this.threshold}px` }
        );
        this.observer.observe(this.sentinel);
    }

    async handleIntersection(entries) {
        if (!entries[0].isIntersecting || this.loading || !this.hasMore) return;

        this.loading = true;
        this.showLoading();
        this.controller = new AbortController();

        try {
            this.page++;
            const data = await this.fetchPage(this.page);
            this.renderItems(data.items);
            this.hasMore = data.hasMore;

            if (!this.hasMore) {
                this.observer.unobserve(this.sentinel);
                this.showEndMessage();
            }
        } catch (err) {
            if (err.name === "AbortError") return;
            this.page--;
            this.showError("Failed to load more items. Try scrolling again.");
        } finally {
            this.controller = null;
            this.loading = false;
            this.hideLoading();
        }
    }

    async fetchPage(pageNum) {
        const url = `${this.fetchUrl}?page=${pageNum}&limit=${this.pageSize}`;
        const res = await fetch(url, { signal: this.controller.signal });
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        return res.json();
    }

    renderItems(items) {
        const fragment = document.createDocumentFragment();
        for (const item of items) {
            fragment.appendChild(this.renderItem(item));
        }
        this.container.appendChild(fragment);
    }

    showLoading() {
        let loader = document.getElementById("scroll-loader");
        if (!loader) {
            loader = document.createElement("div");
            loader.id = "scroll-loader";
            loader.className = "scroll-loader";
            loader.setAttribute("role", "status");
            loader.textContent = "Loading more items…";
            this.container.parentElement.appendChild(loader);
        }
        loader.style.display = "block";
    }

    hideLoading() {
        const loader = document.getElementById("scroll-loader");
        if (loader) loader.style.display = "none";
    }

    showError(message) {
        let error = document.getElementById("scroll-error");
        if (!error) {
            error = document.createElement("div");
            error.id = "scroll-error";
            error.className = "scroll-error";
            error.setAttribute("role", "alert");
            this.container.parentElement.appendChild(error);
        }
        error.textContent = message;
        error.style.display = "block";
        setTimeout(() => { error.style.display = "none"; }, 3000);
    }

    showEndMessage() {
        const end = document.createElement("div");
        end.className = "scroll-end";
        end.textContent = "You're all caught up.";
        this.container.parentElement.appendChild(end);
    }

    destroy() {
        if (this.controller) this.controller.abort();
        if (this.observer) {
            this.observer.disconnect();
            this.observer = null;
        }
    }
}
