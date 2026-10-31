export interface PlatformInfo {
  platform: 'desktop' | 'web';
  version: string;
  standalone: boolean;
  storage: string;
}

export interface SyncBundle {
  format: string;
  version: string;
  exported_at: string;
  platform: 'desktop' | 'web';
  account: {
    username: string;
    displayName: string;
  };
  data: {
    completions: { lesson_id: string; xp: number; created_at: string }[];
    attempts: { id: string; lesson_id: string; passed: number; total: number; results: unknown[]; created_at: string }[];
    drafts: { lesson_id: string; code: string }[];
    projects: { id: string; name: string; language: string; files: unknown[]; revision: number; updated_at: string }[];
    settings: Record<string, unknown>;
  };
  checksum?: string;
}

export function validateSyncBundle(value: unknown): SyncBundle {
  if (!value || typeof value !== 'object') throw new Error('Некорректный файл DevForge');
  const bundle = value as SyncBundle;
  if (bundle.format !== 'devforge-sync' || !/^(?:0\.[45]\.\d+|1\.0\.\d+)$/.test(bundle.version)
    || typeof bundle.checksum !== 'string' || !/^[a-f0-9]{64}$/.test(bundle.checksum)
    || !bundle.account || typeof bundle.account.username !== 'string' || !bundle.data
    || !Array.isArray(bundle.data.completions) || !Array.isArray(bundle.data.projects)
    || !Array.isArray(bundle.data.attempts) || !Array.isArray(bundle.data.drafts)
    || !bundle.data.settings || typeof bundle.data.settings !== 'object' || Array.isArray(bundle.data.settings)) {
    throw new Error('Файл не соответствует формату резервной копии DevForge');
  }
  return bundle;
}

export async function readSyncFile(file: File): Promise<SyncBundle> {
  // Leave room for the JSON request envelope under the server's 7 MB limit.
  if (file.size > 6_500_000) throw new Error('Файл слишком большой: максимум 6,5 МБ');
  return validateSyncBundle(JSON.parse(await file.text()));
}

export class PlatformAdapter {
  static isDesktop(): boolean {
    if (typeof window === 'undefined') return false;
    const nav = window.navigator as { userAgent?: string };
    const isWebView = !!(window as unknown as { chrome?: { webview?: unknown } }).chrome?.webview;
    const hasDesktopFlag = !!(window as unknown as { __DEVFORGE_DESKTOP__?: boolean }).__DEVFORGE_DESKTOP__;
    return isWebView || hasDesktopFlag || (nav.userAgent ? /DevForgeDesktop/i.test(nav.userAgent) : false);
  }

  static async getInfo(): Promise<PlatformInfo> {
    try {
      const res = await fetch('/api/platform');
      if (res.ok) {
        return await res.json();
      }
    } catch {
      // Fallback
    }
    return {
      platform: this.isDesktop() ? 'desktop' : 'web',
      version: '1.0.0',
      standalone: true,
      storage: 'local'
    };
  }

  static downloadFile(filename: string, content: string, mimeType = 'application/json') {
    const blob = new Blob([content], { type: mimeType });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
  }

  static async exportProgress(): Promise<SyncBundle> {
    const res = await fetch('/api/sync/export');
    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: 'Ошибка экспорта' }));
      throw new Error(err.detail || 'Не удалось экспортировать данные');
    }
    const bundle: SyncBundle = await res.json();
    const dateStr = new Date().toISOString().slice(0, 10);
    this.downloadFile(`devforge_backup_v${bundle.version}_${bundle.account.username}_${dateStr}.json`, JSON.stringify(bundle, null, 2));
    return bundle;
  }

  static async importProgressFile(file: File, mode: 'merge' | 'overwrite' = 'merge'): Promise<{ message: string; imported_completions: number; imported_projects: number }> {
    const bundle = await readSyncFile(file);

    const res = await fetch('/api/sync/import', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ bundle, mode })
    });

    if (!res.ok) {
      const err = await res.json().catch(() => ({ detail: 'Ошибка импорта' }));
      throw new Error(err.detail || 'Не удалось импортировать данные');
    }

    return await res.json();
  }
}
