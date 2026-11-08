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


export type RichBlockKind = 'paragraph' | 'horizontalRule';

/**
 * Validate the shape of a controlled block editor after the browser changes
 * its DOM. Text inside paragraphs may change; the sequence of structural
 * blocks must never change outside explicit, model-backed operations.
 */
export function matchesExpectedBlockStructure(
  host: HTMLElement, expected: readonly RichBlockKind[]
): boolean {
  if (!expected.length || expected.length > 1024 || host.children.length !== expected.length) {
    return false;
  }
  // Native contenteditable can occasionally emit stray direct text nodes.
  // Ignore only formatting whitespace, not data outside an expected paragraph.
  for (const node of host.childNodes) {
    if (node.nodeType === Node.TEXT_NODE && (node.textContent ?? '').trim()) return false;
    if (node.nodeType !== Node.TEXT_NODE && node.nodeType !== Node.ELEMENT_NODE) return false;
  }

  for (let index = 0; index < expected.length; index++) {
    const element = host.children.item(index);
    const kind = expected[index];
    if (!(element instanceof HTMLElement)) return false;
    if (kind === 'paragraph') {
      if (element.tagName !== 'P' || element.dataset.richBlock !== 'paragraph') {
        return false;
      }
    } else if (kind === 'horizontalRule') {
      if (element.tagName !== 'HR' ||
          element.dataset.richBlock !== 'horizontalRule' ||
          element.getAttribute('contenteditable') !== 'false') {
        return false;
      }
    } else {
      return false;
    }
  }
  return host.querySelectorAll('hr').length ===
      expected.filter(kind => kind === 'horizontalRule').length &&
    host.querySelectorAll('p').length ===
      expected.filter(kind => kind === 'paragraph').length;
}

/**
 * Experimental recovery boundary for noncancelable edits. The caller MUST
 * provide a restoration function backed by the last validated, versioned
 * document; never restore arbitrary HTML captured from an untrusted DOM.
 *
 * The returned verify() must also run before saving. If restoration fails,
 * verify() returns false so the eventual controller can block persistence.
 */
export function installBlockStructureRecovery(
  host: HTMLElement,
  expected: readonly RichBlockKind[],
  restoreTrustedSnapshot: () => void,
  onViolation: (restored: boolean) => void
): { verify: () => boolean; dispose: () => void } {
  const allowed = [...expected];
  const verify = (): boolean => {
    if (matchesExpectedBlockStructure(host, allowed)) return true;
    let restored = false;
    try {
      restoreTrustedSnapshot();
      restored = matchesExpectedBlockStructure(host, allowed);
    } catch {
      restored = false;
    }
    onViolation(restored);
    return restored;
  };
  const onInput = () => { verify(); };
  host.addEventListener('input', onInput);
  return {
    verify,
    dispose: () => { host.removeEventListener('input', onInput); }
  };
}
