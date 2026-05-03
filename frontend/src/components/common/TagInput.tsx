import { useMemo, useState, type KeyboardEventHandler } from 'react';
import { X } from 'lucide-react';
import { Input } from '@/components/ui/input';
import { cn } from '@/lib/utils';

function normalizeForSearch(value: string): string {
  return value
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
    .trim();
}

function dedupeTags(tags: string[]): string[] {
  const seen = new Set<string>();
  const next: string[] = [];
  for (const raw of tags) {
    const trimmed = raw.trim();
    if (!trimmed) continue;
    const key = normalizeForSearch(trimmed);
    if (seen.has(key)) continue;
    seen.add(key);
    next.push(trimmed);
  }
  return next;
}

export interface TagInputProps {
  id?: string;
  name?: string;
  value: string[];
  onChange: (next: string[]) => void;
  suggestions?: string[];
  disabled?: boolean;
  placeholder?: string;
  maxTags?: number;
  minTagLength?: number;
  maxTagLength?: number;
  suggestionsLimit?: number;
  ariaInvalid?: boolean;
  suggestionsUnavailableMessage?: string;
}

export function TagInput({
  id,
  name,
  value,
  onChange,
  suggestions = [],
  disabled = false,
  placeholder = 'Ajouter un tag',
  maxTags = 15,
  minTagLength = 3,
  maxTagLength = 32,
  suggestionsLimit = 8,
  ariaInvalid = false,
  suggestionsUnavailableMessage,
}: TagInputProps) {
  const [inputValue, setInputValue] = useState('');
  const [highlightedIndex, setHighlightedIndex] = useState(-1);
  const [localError, setLocalError] = useState<string | null>(null);

  const tagSet = useMemo(() => new Set(value.map(normalizeForSearch)), [value]);

  const filteredSuggestions = useMemo(() => {
    const query = normalizeForSearch(inputValue);
    if (!query) return [];

    const ranked = suggestions
      .map((original) => {
        const normalized = normalizeForSearch(original);
        if (!normalized || tagSet.has(normalized) || !normalized.includes(query)) {
          return null;
        }
        const priority = normalized.startsWith(query) ? 0 : 1;
        return { original, normalized, priority };
      })
      .filter((item): item is { original: string; normalized: string; priority: number } => !!item)
      .sort((a, b) => {
        if (a.priority !== b.priority) return a.priority - b.priority;
        return a.normalized.localeCompare(b.normalized, 'fr');
      })
      .slice(0, suggestionsLimit);

    return ranked.map((item) => item.original);
  }, [inputValue, suggestions, suggestionsLimit, tagSet]);

  const clearInput = () => {
    setInputValue('');
    setHighlightedIndex(-1);
    setLocalError(null);
  };

  const addTag = (raw: string) => {
    const trimmed = raw.trim();
    if (!trimmed) return;
    if (trimmed.length < minTagLength) {
      setLocalError(`Un tag doit contenir au moins ${minTagLength} caractères.`);
      return;
    }
    if (trimmed.length > maxTagLength) {
      setLocalError(`Un tag ne peut pas dépasser ${maxTagLength} caractères.`);
      return;
    }
    if (value.length >= maxTags) {
      setLocalError(`Maximum ${maxTags} tags.`);
      return;
    }
    const key = normalizeForSearch(trimmed);
    if (tagSet.has(key)) {
      clearInput();
      return;
    }
    onChange(dedupeTags([...value, trimmed]).slice(0, maxTags));
    clearInput();
  };

  const removeTag = (index: number) => {
    onChange(value.filter((_, i) => i !== index));
  };

  const commitCurrentInput = () => {
    addTag(inputValue);
  };

  const onKeyDown: KeyboardEventHandler<HTMLInputElement> = (event) => {
    if (event.key === 'ArrowDown') {
      if (!filteredSuggestions.length) return;
      event.preventDefault();
      setHighlightedIndex((prev) => (prev + 1) % filteredSuggestions.length);
      return;
    }
    if (event.key === 'ArrowUp') {
      if (!filteredSuggestions.length) return;
      event.preventDefault();
      setHighlightedIndex((prev) => (prev <= 0 ? filteredSuggestions.length - 1 : prev - 1));
      return;
    }
    if (event.key === 'Enter') {
      event.preventDefault();
      if (highlightedIndex >= 0 && filteredSuggestions[highlightedIndex]) {
        addTag(filteredSuggestions[highlightedIndex]);
      } else {
        commitCurrentInput();
      }
      return;
    }
    if (event.key === ',') {
      event.preventDefault();
      commitCurrentInput();
      return;
    }
    if (event.key === 'Backspace' && !inputValue && value.length > 0) {
      event.preventDefault();
      removeTag(value.length - 1);
      return;
    }
    setHighlightedIndex(-1);
  };

  return (
    <div className="space-y-2">
      <div
        className={cn(
          'min-h-10 w-full rounded-md border border-input bg-transparent px-2 py-2',
          ariaInvalid && 'border-destructive'
        )}
      >
        <div className="flex flex-wrap items-center gap-2">
          {value.map((tag, index) => (
            <span
              key={`${tag}-${index}`}
              className="inline-flex items-center gap-1 rounded-full bg-muted px-2 py-1 text-xs font-medium"
            >
              {tag}
              <button
                type="button"
                onClick={() => removeTag(index)}
                disabled={disabled}
                className="text-muted-foreground hover:text-foreground disabled:cursor-not-allowed"
                aria-label={`Retirer ${tag}`}
              >
                <X className="size-3" />
              </button>
            </span>
          ))}
          <Input
            id={id}
            name={name}
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={onKeyDown}
            onBlur={commitCurrentInput}
            placeholder={value.length >= maxTags ? `Maximum ${maxTags} tags` : placeholder}
            disabled={disabled || value.length >= maxTags}
            aria-invalid={ariaInvalid}
            role="combobox"
            aria-expanded={filteredSuggestions.length > 0}
            aria-controls={id ? `${id}-suggestions` : undefined}
            className="h-7 flex-1 border-none bg-transparent p-0 shadow-none focus-visible:ring-0"
          />
        </div>
      </div>

      {inputValue && filteredSuggestions.length > 0 && (
        <ul
          id={id ? `${id}-suggestions` : undefined}
          role="listbox"
          className="max-h-48 overflow-auto rounded-md border bg-card p-1"
        >
          {filteredSuggestions.map((suggestion, index) => (
            <li
              key={`${suggestion}-${index}`}
              role="option"
              aria-selected={index === highlightedIndex}
            >
              <button
                type="button"
                className={cn(
                  'w-full rounded px-2 py-1 text-left text-sm hover:bg-accent',
                  index === highlightedIndex && 'bg-accent'
                )}
                onMouseDown={(e) => e.preventDefault()}
                onClick={() => addTag(suggestion)}
              >
                {suggestion}
              </button>
            </li>
          ))}
        </ul>
      )}

      {localError && <p className="text-xs text-destructive">{localError}</p>}
      {suggestionsUnavailableMessage && (
        <p className="text-xs text-muted-foreground">{suggestionsUnavailableMessage}</p>
      )}
    </div>
  );
}
