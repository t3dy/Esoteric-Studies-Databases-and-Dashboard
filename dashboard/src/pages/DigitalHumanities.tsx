import React, { useEffect, useState } from 'react';
// Inline UI Components for Static Build
const Card = ({ className, children }: any) => <div className={`rounded-lg border shadow-sm ${className}`}>{children}</div>
const CardHeader = ({ className, children }: any) => <div className={`flex flex-col space-y-1.5 p-6 ${className}`}>{children}</div>
const CardTitle = ({ className, children }: any) => <h3 className={`text-2xl font-semibold leading-none tracking-tight ${className}`}>{children}</h3>
const CardContent = ({ className, children }: any) => <div className={`p-6 pt-0 ${className}`}>{children}</div>
const Badge = ({ className, variant, children }: any) => (
    <span className={`inline-flex items-center rounded-full border px-2.5 py-0.5 text-xs font-semibold transition-colors ${className} ${variant === 'outline' ? 'border-amber-400 text-amber-900' : 'bg-amber-700 text-white'}`}>
        {children}
    </span>
);

const DigitalHumanities: React.FC = () => {
    const [pipelineCode, setPipelineCode] = useState<string>("");

    useEffect(() => {
        // In a real app, this would fetch from an endpoint serving the raw file
        // For now, we'll hardcode a snippet or fetch a mocked version
        fetch('/assets/agentic_pipeline.py.txt') // We will need to copy the file here
            .then(res => res.text())
            .then(text => setPipelineCode(text))
            .catch(err => console.error("Failed to load code", err));
    }, []);

    return (
        <div className="p-8 space-y-8 bg-amber-50 min-h-screen font-serif text-slate-900">
            <header className="space-y-4">
                <h1 className="text-4xl font-bold text-amber-900">The Code is the Text</h1>
                <p className="text-xl italic text-amber-800 opacity-80 max-w-2xl">
                    "To understand the historiography of the digital age, one must read the algorithms as primary sources." — Deez Hume, V3 Design Lead
                </p>
            </header>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                {/* Manifesto Column */}
                <div className="space-y-6">
                    <Card className="bg-white/50 border-amber-200">
                        <CardHeader>
                            <CardTitle>Methodological Commitments</CardTitle>
                        </CardHeader>
                        <CardContent className="space-y-4">
                            <div>
                                <h3 className="font-bold text-amber-900">1. Material Intelligence</h3>
                                <p className="text-sm">We treat PDF bytes, OCR errors, and file hashes as historical artifacts, not just data to be cleaned.</p>
                            </div>
                            <div>
                                <h3 className="font-bold text-amber-900">2. Algorithmic Transparency</h3>
                                <p className="text-sm">The logic that defines "Hermeticism" is visible in the Pydantic models below. We hide nothing behind the "AI" curtain.</p>
                            </div>
                            <div>
                                <h3 className="font-bold text-amber-900">3. Retractable Branches</h3>
                                <p className="text-sm">Every interpretive act (mining run) is tagged with a UUID and can be rolled back, preserving the sanctity of the original archive.</p>
                            </div>
                        </CardContent>
                    </Card>

                    <Card className="bg-white/50 border-amber-200">
                        <CardHeader>
                            <CardTitle>System Stats</CardTitle>
                        </CardHeader>
                        <CardContent>
                            <div className="flex flex-wrap gap-2">
                                <Badge variant="outline" className="border-amber-400">Python 3.11</Badge>
                                <Badge variant="outline" className="border-amber-400">SQLite 3.42</Badge>
                                <Badge variant="outline" className="border-amber-400">Pydantic V2</Badge>
                                <Badge variant="outline" className="border-amber-400">React 18</Badge>
                            </div>
                        </CardContent>
                    </Card>
                </div>

                {/* Code Viewer Column */}
                <div className="md:col-span-2 space-y-4">
                    <div className="flex items-center justify-between">
                        <h2 className="text-2xl font-bold text-amber-900">Source: agentic_pipeline.py</h2>
                        <Badge className="bg-amber-700">Live Infrastructure</Badge>
                    </div>

                    <div className="bg-slate-900 text-slate-50 p-6 rounded-lg shadow-inner overflow-x-auto h-[600px] border-4 border-amber-900/10">
                        <pre className="font-mono text-xs leading-relaxed">
                            {pipelineCode || "# Loading strictly typed historiography..."}
                        </pre>
                    </div>

                    <p className="text-center text-sm text-slate-500">
                        *This view renders the actual python file driving the extraction engine.*
                    </p>
                </div>
            </div>
        </div>
    );
};

export default DigitalHumanities;
