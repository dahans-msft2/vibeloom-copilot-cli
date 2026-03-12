const reveals = document.querySelectorAll("[data-reveal]");

const observer = new IntersectionObserver(
  (entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        entry.target.classList.add("is-visible");
        observer.unobserve(entry.target);
      }
    });
  },
  {
    threshold: 0.16,
    rootMargin: "0px 0px -10% 0px",
  }
);

reveals.forEach((node, index) => {
  node.style.transitionDelay = `${Math.min(index * 45, 220)}ms`;
  observer.observe(node);
});
