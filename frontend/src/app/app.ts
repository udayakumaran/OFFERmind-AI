import { Component, OnInit, inject, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { environment } from '../environments/environment';

interface Customer {
  id: number;
  name: string;
  email: string;
  age: number;
  location: string;
  data_gb: number;
  call_mins: number;
  sms_count: number;
}

interface Offer {
  id: number;
  customer_id: number;
  offer_id: number;
  status: string;
  message: string;
}

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, HttpClientModule],
  templateUrl: './app.html',
  styleUrls: ['./app.css']
})
export class App implements OnInit {
  title = 'frontend';
  http = inject(HttpClient);
  cdr = inject(ChangeDetectorRef);
  
  customers: Customer[] = [];
  generatedOffers: Record<number, Offer> = {};
  loading = false;
  activeCustomer: Customer | null = null;
  agentProcessLog: string[] = [];
  
  ngOnInit(): void {
    this.fetchCustomers();
  }

  fetchCustomers() {
    this.loading = true;
    this.http.get<Customer[]>(`${environment.apiUrl}/api/customers`).subscribe({
      next: (data) => {
        console.log('Customers fetched:', data);
        this.customers = data;
        this.loading = false;
        console.log('Component customers set to:', this.customers);
        this.cdr.detectChanges();
      },
      error: (err) => {
        console.error('Error fetching customers', err);
        this.loading = false;
      }
    });
  }

  generateOffer(customerId: number) {
    this.agentProcessLog = [];
    this.activeCustomer = this.customers.find(c => c.id === customerId) || null;
    if (!this.activeCustomer) return;

    this.logStep(`🚀 Initializing LangGraph Orchestrator for ${this.activeCustomer.name}...`);
    
    // Simulate steps graphically
    setTimeout(() => this.logStep(`📊 [Agent 1] Customer Profile Analyzer: Fetching usage data (Data: ${this.activeCustomer?.data_gb}GB, Calls: ${this.activeCustomer?.call_mins}m)`), 500);
    setTimeout(() => this.logStep(`🧠 [Agent 2] Segmentation Agent: Evaluating behavioral patterns and applying rules...`), 1200);
    setTimeout(() => this.logStep(`🎯 [Agent 3] Offer Matching Agent: Finding best personalized product fit...`), 2000);
    setTimeout(() => this.logStep(`✍️ [Agent 4] Personalize Message Agent: Generating natural language pitch...`), 2800);
    
    setTimeout(() => {
      this.http.post<Offer>(`${environment.apiUrl}/api/recommend`, { customer_id: customerId })
        .subscribe({
          next: (offer) => {
            this.generatedOffers[customerId] = offer;
            this.logStep(`✅ Offer generation complete! Assigned Offer #${offer.id}`);
            this.cdr.detectChanges();
          },
          error: (err) => {
            console.error('Error', err);
            this.logStep(`❌ Error: Backend API failed.`);
          }
        });
    }, 3500);
  }

  logStep(msg: string) {
    this.agentProcessLog.push(msg);
    this.cdr.detectChanges();
  }
}
