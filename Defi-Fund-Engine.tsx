import React, { useState, useEffect } from 'react';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, BarChart, Bar } from 'recharts';
import { Calculator, TrendingUp, Shield, Users, DollarSign, Target } from 'lucide-react';

const DeFiFundShowcase = () => {
  const [activeTab, setActiveTab] = useState('overview');
  const [animatedValue, setAnimatedValue] = useState(0);

  // Sample data based on your spreadsheet structure
  const fundPerformanceData = [
    { month: 'M1-3', invested: 72500, commission: 1275, carry: 8244, total: 8244 },
    { month: 'M4-6', invested: 125000, commission: 2500, carry: 12242, total: 20485 },
    { month: 'M7-9', invested: 187500, commission: 1875, carry: 16487, total: 36973 }
  ];

  const carryStructure = [
    { bracket: '$0-$250K', carry: '10%', description: 'Entry level institutional access' },
    { bracket: '$251K-$500K', carry: '15%', description: 'Mid-tier scaling benefits' },
    { bracket: '$501K-$2M', carry: '20%', description: 'Premium tier optimization' }
  ];

  const riskMetrics = {
    projectedReturn1Year: '12%',
    projectedIRR4Years: '115%',
    volatilityManagement: 'Systematic monthly rebalancing',
    regulatoryCompliance: 'SEC/CFTC aligned structure'
  };

  useEffect(() => {
    const timer = setInterval(() => {
      setAnimatedValue(prev => prev < 36973 ? prev + 500 : 36973);
    }, 50);
    return () => clearInterval(timer);
  }, []);

  const TabButton = ({ id, label, icon: Icon }) => (
    <button
      onClick={() => setActiveTab(id)}
      className={`flex items-center space-x-2 px-4 py-2 rounded-lg transition-all ${
        activeTab === id 
          ? 'bg-blue-600 text-white shadow-lg' 
          : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
      }`}
    >
      <Icon size={18} />
      <span>{label}</span>
    </button>
  );

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-800 text-white">
      {/* Header */}
      <div className="bg-black/20 backdrop-blur-sm border-b border-white/10 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-cyan-300 bg-clip-text text-transparent">
                DeFi Fund Management System
              </h1>
              <p className="text-gray-300 mt-1">Systematic Investment Vehicle with Tiered Carry Structure</p>
            </div>
            <div className="text-right">
              <div className="text-3xl font-bold text-green-400">${animatedValue.toLocaleString()}</div>
              <div className="text-sm text-gray-300">Total 3-Year Projected Take</div>
            </div>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <div className="max-w-7xl mx-auto px-6 py-6">
        <div className="flex flex-wrap gap-3 mb-8">
          <TabButton id="overview" label="Executive Summary" icon={Target} />
          <TabButton id="structure" label="Fund Structure" icon={Calculator} />
          <TabButton id="performance" label="Performance Analytics" icon={TrendingUp} />
          <TabButton id="compliance" label="Risk & Compliance" icon={Shield} />
          <TabButton id="technical" label="Technical Implementation" icon={Users} />
        </div>

        {/* Content Sections */}
        {activeTab === 'overview' && (
          <div className="space-y-8">
            <div className="grid md:grid-cols-2 gap-8">
              <div className="bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-white/10">
                <h2 className="text-xl font-semibold mb-4 text-blue-300">Project Innovation</h2>
                <div className="space-y-3 text-gray-300">
                  <p>• <strong>Systematic Capital Deployment:</strong> Monthly investment cycles with scalable intake management</p>
                  <p>• <strong>Tiered Carry Structure:</strong> Performance-based fee optimization across investment brackets</p>
                  <p>• <strong>Risk-Adjusted Returns:</strong> 115% projected 4-year IRR with systematic volatility management</p>
                  <p>• <strong>Regulatory Framework:</strong> Compliant structure designed for institutional scaling</p>
                </div>
              </div>
              
              <div className="bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-white/10">
                <h2 className="text-xl font-semibold mb-4 text-green-300">Business Impact</h2>
                <div className="space-y-4">
                  <div className="flex justify-between">
                    <span>Total Fund Capacity:</span>
                    <span className="font-bold text-green-400">$2M+ per cycle</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Management Fee Revenue:</span>
                    <span className="font-bold text-green-400">$36,973 (9 months)</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Operational Efficiency:</span>
                    <span className="font-bold text-green-400">Automated scaling</span>
                  </div>
                  <div className="flex justify-between">
                    <span>Client Retention:</span>
                    <span className="font-bold text-green-400">3+ year commitments</span>
                  </div>
                </div>
              </div>
            </div>

            <div className="bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-white/10">
              <h2 className="text-xl font-semibold mb-4 text-purple-300">Policy & Regulatory Considerations</h2>
              <div className="grid md:grid-cols-3 gap-6 text-gray-300">
                <div>
                  <h3 className="font-semibold text-white mb-2">Compliance Framework</h3>
                  <p>SEC/CFTC aligned structure with transparent fee disclosure and systematic risk management protocols.</p>
                </div>
                <div>
                  <h3 className="font-semibold text-white mb-2">Investor Protection</h3>
                  <p>Tiered access levels, systematic intake management, and clear performance tracking for enhanced transparency.</p>
                </div>
                <div>
                  <h3 className="font-semibold text-white mb-2">Scalability</h3>
                  <p>Designed for institutional growth with automated processes and regulatory reporting capabilities.</p>
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'structure' && (
          <div className="space-y-8">
            <div className="bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-white/10">
              <h2 className="text-xl font-semibold mb-6 text-blue-300">Tiered Carry Structure</h2>
              <div className="grid md:grid-cols-3 gap-6">
                {carryStructure.map((tier, index) => (
                  <div key={index} className="bg-white/5 rounded-lg p-4 border border-white/10">
                    <div className="text-center">
                      <div className="text-2xl font-bold text-green-400">{tier.carry}</div>
                      <div className="text-sm text-gray-300 mb-2">{tier.bracket}</div>
                      <div className="text-xs text-gray-400">{tier.description}</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-white/10">
              <h2 className="text-xl font-semibold mb-6 text-green-300">Investment Flow Structure</h2>
              <div className="h-80">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={fundPerformanceData}>
                    <CartesianGrid strokeDasharray="3,3" stroke="#374151" />
                    <XAxis dataKey="month" stroke="#9CA3AF" />
                    <YAxis stroke="#9CA3AF" />
                    <Tooltip 
                      contentStyle={{ 
                        backgroundColor: '#1F2937', 
                        border: '1px solid #374151',
                        borderRadius: '8px'
                      }} 
                    />
                    <Bar dataKey="invested" fill="#3B82F6" name="Invested Capital" />
                    <Bar dataKey="carry" fill="#10B981" name="Carry Revenue" />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'performance' && (
          <div className="space-y-8">
            <div className="grid md:grid-cols-2 gap-8">
              <div className="bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-white/10">
                <h2 className="text-xl font-semibold mb-4 text-green-300">Key Performance Metrics</h2>
                <div className="space-y-4">
                  <div className="flex justify-between items-center">
                    <span>1-Year Projected Return:</span>
                    <span className="text-green-400 font-bold">{riskMetrics.projectedReturn1Year}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span>4-Year Projected IRR:</span>
                    <span className="text-green-400 font-bold">{riskMetrics.projectedIRR4Years}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span>Fee Optimization:</span>
                    <span className="text-blue-400 font-bold">2% vs 1% analysis</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span>Capital Efficiency:</span>
                    <span className="text-purple-400 font-bold">Monthly rebalancing</span>
                  </div>
                </div>
              </div>

              <div className="bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-white/10">
                <h2 className="text-xl font-semibold mb-4 text-blue-300">Revenue Projection</h2>
                <div className="h-64">
                  <ResponsiveContainer width="100%" height="100%">
                    <LineChart data={fundPerformanceData}>
                      <CartesianGrid strokeDasharray="3,3" stroke="#374151" />
                      <XAxis dataKey="month" stroke="#9CA3AF" />
                      <YAxis stroke="#9CA3AF" />
                      <Tooltip 
                        contentStyle={{ 
                          backgroundColor: '#1F2937', 
                          border: '1px solid #374151',
                          borderRadius: '8px'
                        }} 
                      />
                      <Line 
                        type="monotone" 
                        dataKey="total" 
                        stroke="#10B981" 
                        strokeWidth={3}
                        name="Cumulative Revenue"
                      />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'compliance' && (
          <div className="space-y-8">
            <div className="bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-white/10">
              <h2 className="text-xl font-semibold mb-6 text-red-300">Risk Management Framework</h2>
              <div className="grid md:grid-cols-2 gap-8">
                <div>
                  <h3 className="font-semibold text-white mb-3">Operational Risk Controls</h3>
                  <ul className="space-y-2 text-gray-300">
                    <li>• Systematic intake volume limits</li>
                    <li>• Monthly investment cycle discipline</li>
                    <li>• Automated rebalancing protocols</li>
                    <li>• Client commitment tracking</li>
                  </ul>
                </div>
                <div>
                  <h3 className="font-semibold text-white mb-3">Regulatory Compliance</h3>
                  <ul className="space-y-2 text-gray-300">
                    <li>• Transparent fee structure disclosure</li>
                    <li>• Performance reporting standards</li>
                    <li>• Investor suitability frameworks</li>
                    <li>• Audit trail maintenance</li>
                  </ul>
                </div>
              </div>
            </div>

            <div className="bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-white/10">
              <h2 className="text-xl font-semibold mb-4 text-yellow-300">Policy Implications</h2>
              <div className="text-gray-300">
                <p className="mb-4">
                  This fund structure demonstrates sophisticated understanding of regulatory requirements
                  while optimizing for operational efficiency and investor protection.
                </p>
                <div className="grid md:grid-cols-2 gap-6">
                  <div>
                    <h4 className="font-semibold text-white mb-2">Regulatory Innovation</h4>
                    <p className="text-sm">Balances growth objectives with compliance requirements through systematic risk management and transparent fee structures.</p>
                  </div>
                  <div>
                    <h4 className="font-semibold text-white mb-2">Market Impact</h4>
                    <p className="text-sm">Scalable model that can accommodate institutional growth while maintaining regulatory compliance and investor protection standards.</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        )}

        {activeTab === 'technical' && (
          <div className="space-y-8">
            <div className="bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-white/10">
              <h2 className="text-xl font-semibold mb-6 text-purple-300">Technical Architecture</h2>
              <div className="grid md:grid-cols-2 gap-8">
                <div>
                  <h3 className="font-semibold text-white mb-3">Core Components</h3>
                  <ul className="space-y-2 text-gray-300">
                    <li>• Excel-based financial modeling system</li>
                    <li>• Automated carry calculation engine</li>
                    <li>• Monthly investment cycle management</li>
                    <li>• Multi-tier fee structure optimization</li>
                  </ul>
                </div>
                <div>
                  <h3 className="font-semibold text-white mb-3">Key Innovations</h3>
                  <ul className="space-y-2 text-gray-300">
                    <li>• Dynamic fee structure based on investment size</li>
                    <li>• Systematic scaling with intake controls</li>
                    <li>• Performance tracking across multiple time horizons</li>
                    <li>• Risk-adjusted return optimization</li>
                  </ul>
                </div>
              </div>
            </div>

            <div className="bg-white/5 backdrop-blur-sm rounded-xl p-6 border border-white/10">
              <h2 className="text-xl font-semibold mb-4 text-cyan-300">Implementation Highlights</h2>
              <div className="bg-gray-900 rounded-lg p-4 font-mono text-sm overflow-x-auto">
                <div className="text-green-400 mb-2">// Fund Performance Calculation Example</div>
                <div className="text-gray-300">
                  <div>carryRate = getCarryByBracket(investmentAmount);</div>
                  <div>projectedReturn = calculateIRR(monthlyInvestment, timeHorizon);</div>
                  <div>totalRevenue = (commissionFees + carryRevenue) * compoundingFactor;</div>
                  <div className="text-blue-400 mt-2">// Risk Management</div>
                  <div>if (monthlyIntake > maxCapacity) limitNewInvestments();</div>
                  <div>if (clientCommitment &lt; 6months) requireExtendedDueDiligence();</div>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Footer */}
      <div className="bg-black/20 backdrop-blur-sm border-t border-white/10 mt-16">
        <div className="max-w-7xl mx-auto px-6 py-8">
          <div className="text-center text-gray-300">
            <p className="mb-2">This showcase demonstrates both technical depth and policy awareness</p>
            <p className="text-sm">Perfect for a hybrid Fintech Policy Lead + Financial Solutions Engineer role</p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DeFiFundShowcase;
