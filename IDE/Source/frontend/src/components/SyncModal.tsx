import { useState, useEffect, useRef } from 'react';
import { Download, Upload, ShieldCheck, RefreshCw, X, Laptop, Globe, AlertCircle, CheckCircle2, History } from 'lucide-react';
import { PlatformAdapter, readSyncFile, type SyncBundle } from '../services/platform';
import { useStore } from '../services/store';
import { api } from '../services/api';

interface SyncModalProps {
  isOpen: boolean;
  onClose: () => void;
}

export default function SyncModal({ isOpen, onClose }: SyncModalProps) {
  const { refresh, notify } = useStore();
  const [isDesktop, setIsDesktop] = useState(false);
  const [busy, setBusy] = useState(false);
  const [preview, setPreview] = useState<SyncBundle | null>(null);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [backups, setBackups] = useState<string[]>([]);
  const [statusMessage, setStatusMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (isOpen) {
      setIsDesktop(PlatformAdapter.isDesktop());
      setStatusMessage(null);
      setPreview(null);
      setSelectedFile(null);
      loadBackups();
    }
  }, [isOpen]);

  async function loadBackups() {
    try {
      const res = await api<{ name: string }[]>('/sync/backups');
      setBackups(res.map(backup => backup.name));
    } catch {
      // ignore
    }
  }

  async function handleExport() {
    setBusy(true);
    setStatusMessage(null);
    try {
      await PlatformAdapter.exportProgress();
      setStatusMessage({ type: 'success', text: 'Файл прогресса успешно скачан в формате JSON!' });
    } catch (e) {
      setStatusMessage({ type: 'error', text: `Ошибка экспорта: ${String(e)}` });
    } finally {
      setBusy(false);
    }
  }

  async function handleFileSelect(e: React.ChangeEvent<HTMLInputElement>) {
    const file = e.target.files?.[0];
    if (!file) return;
    setStatusMessage(null);
    try {
      const bundle = await readSyncFile(file);
      setPreview(bundle);
      setSelectedFile(file);
    } catch (err) {
      setStatusMessage({ type: 'error', text: `Невалидный файл: ${String(err)}` });
      setPreview(null);
      setSelectedFile(null);
    } finally {
      e.target.value = '';
    }
  }

  async function handleApplyImport() {
    if (!selectedFile) return;
    setBusy(true);
    setStatusMessage(null);
    try {
      const result = await PlatformAdapter.importProgressFile(selectedFile);
      await refresh();
      setStatusMessage({
        type: 'success',
        text: `Импорт завершен! Импортировано уроков: ${result.imported_completions}, проектов: ${result.imported_projects}.`
      });
      setPreview(null);
      setSelectedFile(null);
      loadBackups();
      notify('Прогресс успешно синхронизирован!');
    } catch (err) {
      setStatusMessage({ type: 'error', text: `Ошибка импорта: ${String(err)}` });
    } finally {
      setBusy(false);
    }
  }

  if (!isOpen) return null;

  return (
    <div className="modal-overlay" onClick={onClose}>
      <div className="modal-card sync-modal" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <div className="modal-title-wrap">
            <RefreshCw size={22} className="accent-icon" />
            <div>
              <h2>Синхронизация прогресса</h2>
              <p className="modal-subtitle">Перенос обучения между Web-браузером и Desktop-приложением</p>
            </div>
          </div>
          <button className="icon-button close-btn" onClick={onClose} title="Закрыть">
            <X size={18} />
          </button>
        </div>

        <div className="platform-status-banner">
          <div className="platform-tag">
            {isDesktop ? <Laptop size={16} /> : <Globe size={16} />}
            <strong>Текущий режим: {isDesktop ? 'Desktop IDE (WebView2)' : 'Web (Браузер)'}</strong>
          </div>
          <span className="badge-pill">v1.0.0</span>
        </div>

        {statusMessage && (
          <div className={`sync-alert ${statusMessage.type}`}>
            {statusMessage.type === 'success' ? <CheckCircle2 size={18} /> : <AlertCircle size={18} />}
            <span>{statusMessage.text}</span>
          </div>
        )}

        <div className="sync-actions-grid">
          <div className="sync-card">
            <div className="sync-card-icon"><Download size={24} /></div>
            <h3>Экспорт данных</h3>
            <p>Выгрузите все пройденные уроки, историю тестов, черновики кода и лабораторные проекты в единый файл.</p>
            <button className="button primary" disabled={busy} onClick={handleExport}>
              <Download size={16} />
              {busy ? 'Экспорт…' : 'Скачать progress.json'}
            </button>
          </div>

          <div className="sync-card">
            <div className="sync-card-icon"><Upload size={24} /></div>
            <h3>Импорт данных</h3>
            <p>Загрузите ранее сохранённый файл прогресса из другой среды. База данных обновляется с сохранением резервной копии.</p>
            <input
              type="file"
              ref={fileInputRef}
              accept=".json,application/json"
              style={{ display: 'none' }}
              onChange={handleFileSelect}
            />
            <button
              className="button secondary"
              disabled={busy}
              onClick={() => fileInputRef.current?.click()}
            >
              <Upload size={16} />
              Выбрать JSON-файл
            </button>
          </div>
        </div>

        {preview && (
          <div className="sync-preview-box">
            <h4><ShieldCheck size={18} /> Данные готовы к переносу</h4>
            <div className="preview-metrics">
              <div><span>Пользователь:</span> <strong>{preview.account.username}</strong></div>
              <div><span>Пройдено уроков:</span> <strong>{preview.data.completions.length}</strong></div>
              <div><span>Проектов:</span> <strong>{preview.data.projects.length}</strong></div>
              <div><span>Попыток проверок:</span> <strong>{preview.data.attempts.length}</strong></div>
            </div>
            <div className="preview-notice">
              Перед импортом будет автоматически создана точка восстановления в папке <code>data/backups/</code>.
            </div>
            <div className="preview-actions">
              <button className="button primary" disabled={busy} onClick={handleApplyImport}>
                <RefreshCw size={16} />
                {busy ? 'Применение…' : 'Применить и синхронизировать'}
              </button>
              <button className="button tertiary" onClick={() => { setPreview(null); setSelectedFile(null); }}>
                Отмена
              </button>
            </div>
          </div>
        )}

        {backups.length > 0 && (
          <div className="sync-backups-section">
            <div className="backups-title"><History size={15} /> Недавние автоматические резервные копии:</div>
            <ul className="backups-list">
              {backups.slice(0, 3).map((b) => (
                <li key={b}><code>{b}</code></li>
              ))}
            </ul>
          </div>
        )}

        <div className="modal-footer">
          <small className="muted">
            DevForge 1.0.0 единая кодовая база: IDE и Desktop используют совместимый протокол данных.
          </small>
        </div>
      </div>
    </div>
  );
}
