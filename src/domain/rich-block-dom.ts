/**
 * Browser-side safety gate for an experimental segmented block editor.
 * Not imported by the current Conffratus application.
 *
 * A non-editable horizontal rule must never be deleted implicitly when the
 * caret is at the adjacent paragraph boundary. The final editor must also
 * revalidate its model after noncancelable IME/autocorrect input.
 */
function ruleNeighbor(
  host: HTMLElement, atStart: boolean
): boolean {
  const selection = window.getSelection();
  if (!selection?.isCollapsed || !selection.anchorNode) return false;
  const node = selection.anchorNode;
  if (!host.contains(node)) return false;
  const element = node instanceof Element ? node : node.parentElement;
  const paragraph = element?.closest<HTMLElement>('p[data-rich-block="paragraph"]');
  if (!paragraph || !host.contains(paragraph)) return false;

  const neighbor = atStart
    ? paragraph.previousElementSibling
    : paragraph.nextElementSibling;
  if (!(neighbor instanceof HTMLElement) ||
      neighbor.tagName !== 'HR' ||
      neighbor.dataset.richBlock !== 'horizontalRule') return false;

  const range = document.createRange();
  range.selectNodeContents(paragraph);
  try {
    if (atStart) {
      range.setEnd(node, selection.anchorOffset);
    } else {
      range.setStart(node, selection.anchorOffset);
    }
  } catch {
    return false;
  }
  return range.toString().length === 0;
}

/**
 * This prevents the cancelable portion of native deletion. It cannot alone
 * protect against noncancelable input, which requires a versioned model
 * snapshot + restore by the future editor controller.
 */
export function installRuleDeletionGuard(host: HTMLElement): () => void {
  const keydown = (event: KeyboardEvent) => {
    if (event.defaultPrevented || event.altKey || event.ctrlKey || event.metaKey) return;
    const blocked =
      (event.key === 'Backspace' && ruleNeighbor(host, true)) ||
      (event.key === 'Delete' && ruleNeighbor(host, false));
    if (blocked) event.preventDefault();
  };
  const beforeinput = (event: InputEvent) => {
    const blocked =
      (event.inputType === 'deleteContentBackward' && ruleNeighbor(host, true)) ||
      (event.inputType === 'deleteContentForward' && ruleNeighbor(host, false));
    if (blocked && event.cancelable) event.preventDefault();
  };
  host.addEventListener('keydown', keydown);
  host.addEventListener('beforeinput', beforeinput);
  return () => {
    host.removeEventListener('keydown', keydown);
    host.removeEventListener('beforeinput', beforeinput);
  };
}
