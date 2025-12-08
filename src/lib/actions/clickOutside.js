export function clickOutside(node) {
  const handleClick = (event) => {
    if (!node.contains(event.target)) {
      node.dispatchEvent(new CustomEvent('outclick'));
    }
  };

  document.addEventListener('click', handleClick, true); // Use `true` for capture phase

  return {
    destroy() {
      document.removeEventListener('click', handleClick, true);
    },
  };
}