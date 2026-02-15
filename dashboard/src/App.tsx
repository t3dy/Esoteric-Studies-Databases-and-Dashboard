import { useState, useEffect } from 'react';
import axios from 'axios';
import {
  Search, Book, X, Plus, FileText, ImageIcon,
  MessageSquare, Library
} from 'lucide-react';
import {
  ResponsiveContainer, BarChart, Bar, XAxis, YAxis, Tooltip,
  CartesianGrid, PieChart, Pie, Cell, AreaChart, Area
} from 'recharts';
import './index.css';

import DigitalHumanities from './pages/DigitalHumanities';
import ImageGallery from './pages/ImageGallery';

const API_BASE = 'http://localhost:8000/api';

interface Category {
  id: number;
  name: string;
  type: 'scholar' | 'topic' | 'other';
  is_esoteric: boolean;
}

interface Title {
  id: number;
  title: string;
  path: string;
  category_name: string;
  category_type: string;
  summary?: string;
  media?: any[];
}

interface AlchemyEntity {
  id: string;
  category: string;
  canonical_name: string;
  normalized_name: string;
  metadata_json: string;
  historiography_tags?: string;
  material_alignment?: string;
}

interface AlchemyMention {
  id: number;
  entity_id: string;
  doc_title: string;
  page_hint: number;
  context_snippet: string;
  confidence: number;
}

function App() {
  const [showView, setShowView] = useState<'library' | 'knowledge' | 'questions' | 'popularity' | 'other' | 'all' | 'designers' | 'alchemy' | 'dh' | 'gallery'>('library');
  const [stats, setStats] = useState<any>({ titles: 0, categories: 0, media: 0, chats: 0, questions: 0 });
  const [alchemyStats] = useState<any>(null);
  const [alchemyEntities] = useState<AlchemyEntity[]>([]);
  const [selectedAlchemyEntity] = useState<AlchemyEntity | null>(null);
  const [alchemyMentions] = useState<AlchemyMention[]>([]);
  const [selectedAlchemyCat, setSelectedAlchemyCat] = useState<string>('ALCHEMISTS');
  const [miningStatus] = useState<string>('');
  const [newMediaPath, setNewMediaPath] = useState('');
  const [newMediaType, setNewMediaType] = useState('image');

  const [categories] = useState<Category[]>([]);
  const [titles] = useState<Title[]>([]);
  // ... rest of state
  const [scholars] = useState<{ id: string, name: string }[]>([]);
  const [chats, setChats] = useState<{ id: number, title: string, date: string, model: string, msg_count: number }[]>([]);
  const [questions, setQuestions] = useState<{ id: number, text: string, move: string, chat_title: string, chat_id: number }[]>([]);
  const [inquiryStats, setInquiryStats] = useState<any>(null);
  const [designers, setDesigners] = useState<any[]>([]);
  const [selectedDesigner, setSelectedDesigner] = useState<any | null>(null);

  const [selectedCategory, setSelectedCategory] = useState<number | null>(null);
  const [searchQuery, setSearchQuery] = useState('');
  const [selectedTitleId, setSelectedTitleId] = useState<number | null>(null);
  const [titleDetail] = useState<Title | null>(null);
  const [selectedScholar, setSelectedScholar] = useState<string | null>(null);
  const [selectedChat, setSelectedChat] = useState<any | null>(null);
  const [selectedMove, setSelectedMove] = useState<string | null>(null);
  const [loading] = useState(false);

  useEffect(() => {
    // Check for query param 'view'
    const params = new URLSearchParams(window.location.search);
    const view = params.get('view');
    if (view && ['library', 'knowledge', 'questions', 'popularity', 'other', 'all', 'designers', 'alchemy', 'dh', 'gallery'].includes(view)) {
      setShowView(view as any);
    }

    // STATIC MODE: Fetch from JSON snapshots
    // In production (GitHub Pages), we read from relative path
    const STATIC_BASE = import.meta.env.BASE_URL + 'data/latest/';

    const loadStaticData = async () => {
      try {
        console.log("Loading Static Data from:", STATIC_BASE);
        const s = await axios.get(STATIC_BASE + 'stats.json');
        setStats(s.data);

        // For now, minimal load
      } catch (e) {
        console.error("Failed to load static snapshots. Are they exported?", e);
      }
    };

    loadStaticData();

    // fetchStats(); // Disable Live API
    // fetchCategories();
    // fetchScholars();
    // fetchAlchemyStats();
  }, []);

  useEffect(() => {
    if (showView === 'knowledge') {
      fetchChats();
    } else if (showView === 'questions') {
      fetchQuestions();
      fetchInquiryStats();
    } else if (showView === 'popularity') {
      fetchInquiryStats();
    } else if (showView === 'designers') {
      fetchDesigners();
    } else if (showView === 'alchemy') {
      fetchAlchemyEntities(selectedAlchemyCat);
      fetchAlchemyStats();
    } else if (showView === 'other') {
      fetchTitles(0);
    } else if (showView === 'all') {
      fetchTitles();
    } else {
      fetchTitles(1);
    }
  }, [selectedCategory, searchQuery, showView, selectedScholar, selectedMove, selectedAlchemyCat]);

  /*
  const fetchAlchemyStats = async () => {
    try {
      const res = await axios.get(`${API_BASE}/alchemy/stats`);
      setAlchemyStats(res.data);
    } catch (e) { console.error(e); }
  };
  */

  const fetchAlchemyEntities = async (cat: string) => {
    // ... logic
  };

  const fetchAlchemyEntityDetail = async (id: string) => {
    // ... logic
  };

  const triggerMining = async () => {
    // ... logic
  };

  /*
  const fetchStats = async () => {
    try {
      const res = await axios.get(`${API_BASE}/stats`);
      setStats(res.data);
    } catch (e) { console.error(e); }
  };
  */

  // ... (rest of fetchers)

  /*
  const fetchCategories = async () => {
    try {
      const res = await axios.get(`${API_BASE}/categories`);
      setCategories(res.data);
    } catch (err) { console.error(err); }
  };
  */

  const fetchTitles = async (esotericOnly?: number) => {
    // ... logic
  };

  const fetchTitleDetail = async (id: number) => {
    // ... logic
  };

  /* 
  const fetchScholars = async () => {
    try {
      const res = await axios.get(`${API_BASE}/knowledge/scholars`);
      setScholars(res.data);
    } catch (err) { console.error(err); }
  };
  */

  const fetchChats = async () => {
    try {
      const res = await axios.get(`${API_BASE}/knowledge/chats`, {
        params: { scholar_id: selectedScholar }
      });
      setChats(res.data);
    } catch (err) { console.error(err); }
  };

  const fetchQuestions = async () => {
    try {
      const res = await axios.get(`${API_BASE}/knowledge/questions`, {
        params: { move_type: selectedMove }
      });
      setQuestions(res.data);
    } catch (err) { console.error(err); }
  };

  const fetchInquiryStats = async () => {
    try {
      const res = await axios.get(`${API_BASE}/knowledge/inquiry-stats`);
      setInquiryStats(res.data);
    } catch (err) { console.error(err); }
  };

  const fetchDesigners = async () => {
    try {
      const res = await axios.get(`${API_BASE}/designers`);
      setDesigners(res.data);
      if (res.data.length > 0 && !selectedDesigner) setSelectedDesigner(res.data[0]);
    } catch (err) { console.error(err); }
  };

  const fetchChatDetails = async (id: number) => {
    try {
      const res = await axios.get(`${API_BASE}/knowledge/chats/${id}`);
      setSelectedChat(res.data);
    } catch (err) { console.error(err); }
  };

  const handleAddMedia = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedTitleId || !newMediaPath) return;

    try {
      await axios.post(`${API_BASE}/media`, {
        title_id: selectedTitleId,
        media_path: newMediaPath,
        media_type: newMediaType
      });
      setNewMediaPath('');
      fetchTitleDetail(selectedTitleId);
    } catch (err) {
      alert("Error adding media");
    }
  };



  return (
    <div className="app-container">
      {/* Sidebar */}
      <aside className="sidebar">
        <div className="logo">
          <Library size={32} color="#d4af37" />
          <h1 onClick={() => {
            const newTheme = document.documentElement.getAttribute('data-theme') === 'grimoire' ? 'light' : 'grimoire';
            document.documentElement.setAttribute('data-theme', newTheme);
          }} style={{ cursor: 'pointer' }} title="Toggle Lumina Theme">Esoteric Studies</h1>
        </div>

        <div className="view-toggle">
          <button
            className={showView === 'library' ? 'active' : ''}
            onClick={() => setShowView('library')}
          >
            Esoteric
          </button>
          <button
            className={showView === 'other' ? 'active' : ''}
            onClick={() => setShowView('other')}
          >
            Other
          </button>
          <button
            className={showView === 'knowledge' ? 'active' : ''}
            onClick={() => setShowView('knowledge')}
          >
            Archive
          </button>
        </div>

        <div className="nav-section">
          <h3>Tools</h3>
          <div className="category-list">
            <button className={showView === 'questions' ? 'active' : ''} onClick={() => setShowView('questions')}>Question Explore</button>
            <button className={showView === 'popularity' ? 'active' : ''} onClick={() => setShowView('popularity')}>Popularity Contest</button>
            <button className={showView === 'all' ? 'active' : ''} onClick={() => setShowView('all')}>Full Search</button>
            <button className={showView === 'designers' ? 'active' : ''} onClick={() => setShowView('designers')}>Hall of Designers</button>
            <button className={showView === 'dh' ? 'active' : ''} onClick={() => setShowView('dh')} style={{ color: '#d4af37' }}>Digital Humanities</button>
            <button className={showView === 'gallery' ? 'active' : ''} onClick={() => setShowView('gallery')}>Image Vault</button>
            <button className={showView === 'alchemy' ? 'active' : ''} onClick={() => setShowView('alchemy')} style={{ color: 'var(--accent-color)' }}>Alchemy Portal</button>
          </div>
        </div>

        <div className="stats-box">
          <div className="stat"><span>Volumes</span> <strong>{stats.titles}</strong></div>
          <div className="stat"><span>Chats</span> <strong>{stats.chats}</strong></div>
          <div className="stat"><span>Questions</span> <strong>{stats.questions}</strong></div>
          {alchemyStats && <div className="stat"><span>Alchemy</span> <strong>{alchemyStats.total_mentions}</strong></div>}
        </div>

        <div className="nav-section">
          <h3>
            {(showView === 'library' || showView === 'other' || showView === 'all') ? 'Filtering' :
              showView === 'knowledge' ? 'Scholars' :
                'Inquiry Moves'}
          </h3>
          <div className="category-list">
            {(showView === 'library' || showView === 'other' || showView === 'all') ? (
              <>
                <button
                  className={selectedCategory === null ? 'active' : ''}
                  onClick={() => setSelectedCategory(null)}
                >
                  All Categories
                </button>
                {categories.filter(c => showView === 'all' || (showView === 'library' ? c.is_esoteric : !c.is_esoteric)).map(c => (
                  <button
                    key={c.id}
                    className={selectedCategory === c.id ? 'active' : ''}
                    onClick={() => setSelectedCategory(c.id)}
                  >
                    {c.name}
                  </button>
                ))}
              </>
            ) : showView === 'knowledge' ? (
              <>
                <button
                  className={selectedScholar === null ? 'active' : ''}
                  onClick={() => setSelectedScholar(null)}
                >
                  All Scholars
                </button>
                {scholars.map(s => (
                  <button
                    key={s.id}
                    className={selectedScholar === s.id ? 'active' : ''}
                    onClick={() => setSelectedScholar(s.id)}
                  >
                    {s.name}
                  </button>
                ))}
              </>
            ) : (
              <>
                <button
                  className={selectedMove === null ? 'active' : ''}
                  onClick={() => setSelectedMove(null)}
                >
                  All Moves
                </button>
                {["Table Generation", "Summarization", "Methodology Analysis", "Bibliographic Inquiry", "Conceptual Analysis", "General Question"].map(m => (
                  <button
                    key={m}
                    className={selectedMove === m ? 'active' : ''}
                    onClick={() => setSelectedMove(m)}
                  >
                    {m}
                  </button>
                ))}
              </>
            )}
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="main-content">
        <header className="header">
          <div className="search-container">
            <Search className="search-icon" size={18} />
            <input
              type="text"
              className="search-input"
              placeholder={`Search ${showView}...`}
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>
          <div className="stats">
            {loading && (showView === 'library' || showView === 'other' || showView === 'all') ? 'Searching...' : (showView === 'library' || showView === 'other' || showView === 'all') ? `${titles.length} titles shown` : ''}
            {loading && showView === 'knowledge' ? 'Searching...' : showView === 'knowledge' ? `${chats.length} chats shown` : ''}
            {loading && showView === 'questions' ? 'Searching...' : showView === 'questions' ? `${questions.length} questions shown` : ''}
          </div>
        </header>

        {(showView === 'library' || showView === 'other' || showView === 'all') && (
          <div className="grid-container">
            {titles.map(title => (
              <div key={title.id} className="card" onClick={() => setSelectedTitleId(title.id)}>
                <span className={`badge badge-${title.category_type}`}>
                  {title.category_name}
                </span>
                <h3>{title.title}</h3>
                <div className="card-meta">
                  <div style={{ display: 'flex', alignItems: 'center', gap: '4px' }}>
                    <Book size={12} />
                    <span>PDF Document</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}

        {showView === 'knowledge' && (
          <div className="chat-grid">
            {chats.filter(c => c.title.toLowerCase().includes(searchQuery.toLowerCase())).map(c => (
              <div key={c.id} className="chat-card" onClick={() => fetchChatDetails(c.id)}>
                <div className="card-header">
                  <MessageSquare size={24} />
                  <span className="model-badge">{c.model}</span>
                </div>
                <h3>{c.title}</h3>
                <div className="chat-meta">
                  <span>{c.date}</span>
                  <span>{c.msg_count} msgs</span>
                </div>
              </div>
            ))}
          </div>
        )}

        {showView === 'questions' && (
          <div className="questions-view">
            {inquiryStats && (
              <section className="viz-section">
                <h3>Inquiry Density (Questions per Chat)</h3>
                <div style={{ width: '100%', height: 300, background: '#1a1a1a', padding: '20px', borderRadius: '12px' }}>
                  <ResponsiveContainer width="100%" height="100%">
                    <BarChart data={inquiryStats.chat_stats.slice(0, 20)}>
                      <XAxis dataKey="title" hide />
                      <YAxis stroke="#888" />
                      <Tooltip contentStyle={{ background: '#222', border: '1px solid #333' }} />
                      <Bar dataKey="count" fill="#d4af37" radius={[4, 4, 0, 0]} />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </section>
            )}

            <div className="question-list">
              {questions.filter(q => q.text.toLowerCase().includes(searchQuery.toLowerCase())).map(q => (
                <div key={q.id} className="question-item" onClick={() => fetchChatDetails(q.chat_id)}>
                  <div className="item-meta">
                    <span className={`move-badge ${q.move.toLowerCase().replace(' ', '-')}`}>
                      {q.move}
                    </span>
                    <span className="chat-ref">{q.chat_title}</span>
                  </div>
                  <p className="question-text">{q.text}</p>
                </div>
              ))}
            </div>
          </div>
        )}

        {showView === 'popularity' && inquiryStats && (
          <div className="popularity-dashboard">
            <div className="popularity-grid">
              <section className="viz-card">
                <h3>Top Topics by Volume</h3>
                <div className="chart-container">
                  <ResponsiveContainer width="100%" height={300}>
                    <BarChart data={inquiryStats.popularity.categories}>
                      <CartesianGrid strokeDasharray="3 3" stroke="#333" />
                      <XAxis dataKey="name" stroke="#888" hide />
                      <YAxis stroke="#888" />
                      <Tooltip contentStyle={{ background: '#222', border: '1px solid #444' }} />
                      <Bar dataKey="volumes" fill="#d4af37" />
                    </BarChart>
                  </ResponsiveContainer>
                </div>
              </section>

              <section className="viz-card">
                <h3>Scholar Inquiry (Chat Mentions)</h3>
                <div className="chart-container">
                  <ResponsiveContainer width="100%" height={300}>
                    <PieChart>
                      <Pie
                        data={inquiryStats.popularity.scholars}
                        dataKey="chats"
                        nameKey="name"
                        cx="50%"
                        cy="50%"
                        outerRadius={80}
                        label
                      >
                        {inquiryStats.popularity.scholars.map((_: any, index: number) => (
                          <Cell key={`cell-${index}`} fill={['#d4af37', '#4cc9f0', '#f72585', '#7b2ff7', '#4caf50'][index % 5]} />
                        ))}
                      </Pie>
                      <Tooltip />
                    </PieChart>
                  </ResponsiveContainer>
                </div>
              </section>
            </div>

            <section className="move-density">
              <h3>Question Density across Archive</h3>
              <div className="chart-container">
                <ResponsiveContainer width="100%" height={300}>
                  <AreaChart data={inquiryStats.chat_stats.slice(0, 30)}>
                    <XAxis dataKey="title" hide />
                    <YAxis />
                    <Tooltip />
                    <Area type="monotone" dataKey="count" stroke="#d4af37" fill="rgba(212, 175, 55, 0.2)" />
                  </AreaChart>
                </ResponsiveContainer>
              </div>
            </section>
          </div>
        )}

        {showView === 'designers' && (
          <div className="designers-page">
            <header className="page-intro">
              <h2 style={{ color: '#d4af37' }}>The Hall of Designers</h2>
              <p>Meet the Renaissance minds architecting your esoteric research engine.</p>
            </header>

            <div className="designer-selector">
              {designers.map(d => (
                <button
                  key={d.id}
                  className={`designer-btn ${selectedDesigner?.id === d.id ? 'active' : ''}`}
                  onClick={() => setSelectedDesigner(d)}
                >
                  <div className="designer-avatar">{d.name[0]}</div>
                  <div className="designer-info">
                    <span className="d-name">{d.name}</span>
                    <span className="d-role">{d.role}</span>
                  </div>
                </button>
              ))}
            </div>

            {selectedDesigner && (
              <div className="designer-details animate-in">
                <div className="designer-column">
                  <section className="designer-issues">
                    <h3>Focus & Tracking (Current Issues)</h3>
                    <ul className="issue-list">
                      {selectedDesigner.issues.map((issue: string, idx: number) => (
                        <li key={idx} className="issue-item">
                          <Plus size={14} color="#d4af37" />
                          <span>{issue}</span>
                        </li>
                      ))}
                    </ul>
                  </section>
                </div>

                <div className="designer-column">
                  <section className="architectural-flow">
                    <h3>Architectural Blueprint: {selectedDesigner.role}</h3>
                    <div className="blueprint-box">
                      <Mermaid chart={selectedDesigner.flow} key={selectedDesigner.id} />
                    </div>
                  </section>
                </div>
              </div>
            )}
          </div>
        )}

        {showView === 'alchemy' && (
          <div className="alchemy-portal">
            <header className="portal-header">
              <div>
                <h2 style={{ color: 'var(--accent-color)', marginBottom: '0.5rem' }}>Alchemy Datamine</h2>
                <div className="category-tabs">
                  {['THEORIES', 'ALCHEMISTS', 'EQUIPMENT', 'MATERIALS', 'PROCESSES', 'MOVEMENTS', 'PERIODS', 'ALLEGORIES', 'IMAGES', 'ARTISANAL', 'TEXTS', 'I', 'J'].map(cat => (
                    <button
                      key={cat}
                      className={`category-tab ${selectedAlchemyCat === cat ? 'active' : ''}`}
                      onClick={() => setSelectedAlchemyCat(cat)}
                    >
                      {cat === 'I' ? 'EXPERIMENTS' : cat === 'J' ? 'RECONSTRUCTIONS' : cat}
                    </button>
                  ))}
                </div>
              </div>
              <div style={{ display: 'flex', gap: '1rem', alignItems: 'center' }}>
                {miningStatus && <span style={{ fontSize: '0.8rem', opacity: 0.7 }}>{miningStatus}</span>}
                <button className="mine-btn" onClick={triggerMining}>Run Mine</button>
              </div>
            </header>

            <div className="alchemy-content">
              <div className="entity-pane">
                {alchemyEntities.map(ent => (
                  <div
                    key={ent.id}
                    className={`entity-list-item ${selectedAlchemyEntity?.id === ent.id ? 'active' : ''}`}
                    onClick={() => fetchAlchemyEntityDetail(ent.id)}
                  >
                    <span className="entity-title">{ent.canonical_name}</span>
                    <div className="entity-meta">
                      <span>{ent.category}</span>
                    </div>
                  </div>
                ))}
              </div>

              <div className="evidence-pane">
                {selectedAlchemyEntity ? (
                  <>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <h3>Provenance: {selectedAlchemyEntity.canonical_name}</h3>
                      <div className="hist-tags">
                        {selectedAlchemyEntity.historiography_tags && JSON.parse(selectedAlchemyEntity.historiography_tags).map((tag: string) => (
                          <span key={tag} className={`tag tag-${tag}`}>{tag.replace('_', ' ')}</span>
                        ))}
                      </div>
                    </div>
                    {alchemyMentions.map(m => (
                      <div key={m.id} className="mention-card">
                        <p className="mention-context">{m.context_snippet}</p>
                        <div className="mention-source">
                          <Book size={12} />
                          <span>{m.doc_title} (Page {m.page_hint})</span>
                        </div>
                      </div>
                    ))}
                    {alchemyMentions.length === 0 && <p>No mentions found for this entity.</p>}
                  </>
                ) : (
                  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'center', height: '100%', color: 'var(--text-secondary)' }}>
                    Select an entity to view evidence
                  </div>
                )}
              </div>
            </div>
          </div>
        )}
      </main>

      {showView === 'dh' && (
        <div className="dh-overlay" style={{ position: 'absolute', top: 0, left: '260px', right: 0, bottom: 0, overflow: 'auto', zIndex: 10 }}>
          <DigitalHumanities />
        </div>
      )}

      {showView === 'gallery' && (
        <div className="gallery-overlay" style={{ position: 'absolute', top: 0, left: '260px', right: 0, bottom: 0, overflow: 'auto', zIndex: 10 }}>
          <ImageGallery />
        </div>
      )}

      {/* Main Content End */}

      {/* Title Details Modal */}
      {selectedTitleId && titleDetail && (
        <div className="modal-overlay" onClick={() => setSelectedTitleId(null)}>
          <div className="modal-content" onClick={e => e.stopPropagation()}>
            <button className="close-btn" onClick={() => setSelectedTitleId(null)}>
              <X size={24} />
            </button>
            <div className="modal-header">
              <span className={`badge badge-${titleDetail.category_type}`}>
                {titleDetail.category_name}
              </span>
              <h2>{titleDetail.title}</h2>
              <p style={{ color: 'var(--text-secondary)' }}>{titleDetail.path}</p>
            </div>

            <div className="modal-body">
              <div className="section">
                <p className="section-label">Summary</p>
                <div style={{ backgroundColor: 'var(--bg-color)', padding: '1rem', borderRadius: '8px', border: '1px solid var(--border-color)' }}>
                  {titleDetail.summary || "No summary available. Run AI Agent to generate."}
                </div>
              </div>

              <div className="section" style={{ marginTop: '2rem' }}>
                <p className="section-label">Associated Media</p>
                <div className="media-list">
                  {titleDetail.media?.length === 0 && <p style={{ color: 'var(--text-secondary)' }}>No associated files.</p>}
                  {titleDetail.media?.map(m => (
                    <div key={m.id} className="media-card">
                      <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '4px' }}>
                        {m.media_type === 'image' ? <ImageIcon size={14} /> : <FileText size={14} />}
                        <span style={{ fontWeight: '600' }}>{m.media_type}</span>
                      </div>
                      <p style={{ fontSize: '0.7rem', opacity: 0.7, wordBreak: 'break-all' }}>{m.media_path}</p>
                    </div>
                  ))}
                </div>
              </div>

              <form className="add-media-form" onSubmit={handleAddMedia}>
                <p className="section-label">Link New Media</p>
                <div style={{ display: 'flex', gap: '1rem', alignItems: 'flex-end' }}>
                  <div className="form-group" style={{ flexGrow: 1 }}>
                    <label style={{ fontSize: '0.75rem' }}>File Path</label>
                    <input
                      type="text"
                      className="input-field"
                      placeholder="C:\path\to\character_sketch.png"
                      value={newMediaPath}
                      onChange={e => setNewMediaPath(e.target.value)}
                    />
                  </div>
                  <div className="form-group" style={{ width: '120px' }}>
                    <label style={{ fontSize: '0.75rem' }}>Type</label>
                    <select
                      className="input-field"
                      value={newMediaType}
                      onChange={e => setNewMediaType(e.target.value)}
                    >
                      <option value="image">Image</option>
                      <option value="note">Note</option>
                      <option value="video">Video</option>
                      <option value="other">Other</option>
                    </select>
                  </div>
                  <button type="submit" className="btn-primary" style={{ height: '40px', marginTop: '0', display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <Plus size={16} /> Link
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
      {/* Chat Details Modal */}
      {selectedChat && (
        <div className="modal-overlay" onClick={() => setSelectedChat(null)}>
          <div className="modal-content chat-modal" onClick={e => e.stopPropagation()}>
            <button className="close-btn" onClick={() => setSelectedChat(null)}>
              <X size={24} />
            </button>
            <div className="modal-header">
              <span className="model-badge">{selectedChat.model}</span>
              <h2>{selectedChat.title}</h2>
              <div className="chat-meta">
                <span>{selectedChat.date}</span>
                <span>{selectedChat.msg_count} messages</span>
              </div>
            </div>
            <div className="chat-container">
              {selectedChat.messages.map((m: any, idx: number) => (
                <div key={idx} className={`chat-message ${m.role}`}>
                  <div className="role-label">{m.role}</div>
                  <div className="bubble-content" dangerouslySetInnerHTML={{ __html: m.content }} />
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

function Mermaid({ chart }: { chart: string }) {
  useEffect(() => {
    // @ts-ignore
    if (window.mermaid) {
      // @ts-ignore
      window.mermaid.contentLoaded();
    }
  }, [chart]);

  return <div className="mermaid">{chart}</div>;
}

export default App;
