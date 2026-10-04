"""
Sample dataset generator for the Customer Support Platform
"""
import json
import csv
import os
from datetime import datetime, timedelta
from typing import List, Dict, Any
import random


class SampleDatasetGenerator:
    """Generate sample data for the platform"""
    
    # Sample data templates
    CUSTOMER_NAMES = [
        "John Smith", "Sarah Johnson", "Michael Brown", "Emily Davis",
        "Robert Wilson", "Lisa Anderson", "James Taylor", "Jennifer White",
        "David Martinez", "Mary Thompson"
    ]
    
    SAMPLE_TICKETS = [
        {
            "ticket_type": "delivery",
            "subjects": [
                "Order not delivered yet",
                "Package damaged during delivery",
                "Wrong item received",
                "Delivery address was incorrect"
            ],
            "descriptions": [
                "My order (ORD-123456) was supposed to arrive 3 days ago but I still haven't received it. The tracking shows it's out for delivery but nothing has arrived.",
                "The package arrived but the item inside was completely broken. This is the second time this has happened.",
                "I ordered a blue shirt but received a red one instead. This is very frustrating.",
                "The delivery company delivered to the wrong address and I had to go pick it up."
            ]
        },
        {
            "ticket_type": "refund",
            "subjects": [
                "Request refund for defective product",
                "Want to return my order",
                "Refund status inquiry",
                "Getting refund for wrong item"
            ],
            "descriptions": [
                "The product stopped working after 2 days. I want a full refund please.",
                "I ordered the wrong size and want to return it. Please let me know the process.",
                "I returned my item a week ago but I haven't received my refund yet. Can you check the status?",
                "I need to return the item I received in error and get a refund."
            ]
        },
        {
            "ticket_type": "payment",
            "subjects": [
                "Payment was declined",
                "Charged twice for one order",
                "Payment not processed correctly",
                "Wrong amount charged"
            ],
            "descriptions": [
                "My credit card was declined even though I have sufficient funds. I tried 3 times and got charged 3 times somehow.",
                "I see two charges on my account for the same order number. This needs to be reversed immediately.",
                "The payment failed but I was still charged. Please refund me.",
                "I was charged $500 instead of $50. Please fix this billing error urgently."
            ]
        },
        {
            "ticket_type": "product_issue",
            "subjects": [
                "Product quality is poor",
                "Item is not as described",
                "Parts are missing",
                "Product defective on arrival"
            ],
            "descriptions": [
                "The product quality is much worse than the images on the website. The material feels cheap.",
                "The description said 'premium quality' but it looks like a budget item. Very disappointed.",
                "The package contained only half the parts needed to assemble the furniture.",
                "The item arrived with a factory defect that makes it unusable."
            ]
        },
        {
            "ticket_type": "account",
            "subjects": [
                "Cannot login to my account",
                "Want to change password",
                "Account was hacked",
                "Need to update profile information"
            ],
            "descriptions": [
                "I can't login to my account. The password reset link isn't working.",
                "I need to change my password for security reasons. Can't find where to do this.",
                "Someone accessed my account and made unauthorized purchases. Please help!",
                "I need to update my address and payment method in my profile."
            ]
        },
        {
            "ticket_type": "order_tracking",
            "subjects": [
                "Where is my order",
                "Order status not updated",
                "Tracking number not working",
                "When will my order arrive"
            ],
            "descriptions": [
                "I placed an order but can't find the tracking information. How do I track my package?",
                "The tracking shows 'in transit' for 5 days now. Is there a problem?",
                "The tracking number provided isn't working on any carrier website.",
                "My order shows ready for shipment but I need it by tomorrow."
            ]
        }
    ]
    
    @staticmethod
    def generate_tickets(count: int = 100) -> List[Dict[str, Any]]:
        """Generate sample tickets"""
        tickets = []
        
        for i in range(count):
            ticket_template = random.choice(SampleDatasetGenerator.SAMPLE_TICKETS)
            customer_name = random.choice(SampleDatasetGenerator.CUSTOMER_NAMES)
            
            ticket = {
                "id": f"ticket_{i+1}",
                "ticket_number": f"TKT-{datetime.now().strftime('%Y%m%d')}-{i+1:04d}",
                "customer_name": customer_name,
                "customer_email": f"{customer_name.lower().replace(' ', '_')}@example.com",
                "subject": random.choice(ticket_template["subjects"]),
                "description": random.choice(ticket_template["descriptions"]),
                "category": ticket_template["ticket_type"],
                "priority": random.choice(["low", "medium", "high", "critical"]),
                "status": random.choice(["open", "in_progress", "resolved", "escalated"]),
                "created_at": (datetime.now() - timedelta(days=random.randint(0, 30))).isoformat(),
                "resolved_at": (datetime.now() - timedelta(days=random.randint(0, 30))).isoformat() if random.random() > 0.3 else None,
                "sentiment": random.choice(["very_negative", "negative", "neutral", "positive"]),
            }
            tickets.append(ticket)
        
        return tickets
    
    @staticmethod
    def generate_faqs() -> List[Dict[str, str]]:
        """Generate sample FAQs"""
        faqs = [
            {
                "question": "How do I track my order?",
                "answer": "You can track your order using the tracking number sent to your email. Visit the carrier's website or use our order tracking page.",
                "category": "order_tracking"
            },
            {
                "question": "What is your return policy?",
                "answer": "We accept returns within 30 days of purchase. The item must be in original condition. Shipping costs are the customer's responsibility.",
                "category": "refund"
            },
            {
                "question": "How long does shipping take?",
                "answer": "Standard shipping takes 5-7 business days. Express shipping takes 2-3 business days. International orders may take 2-4 weeks.",
                "category": "delivery"
            },
            {
                "question": "Do you offer international shipping?",
                "answer": "Yes, we ship to over 150 countries. Shipping costs and delivery times vary by location.",
                "category": "delivery"
            },
            {
                "question": "How do I cancel my order?",
                "answer": "Orders can be cancelled within 24 hours of placement if they haven't shipped yet. Contact our support team for assistance.",
                "category": "order_tracking"
            },
            {
                "question": "What payment methods do you accept?",
                "answer": "We accept all major credit cards, PayPal, Apple Pay, and Google Pay.",
                "category": "payment"
            },
            {
                "question": "Is my payment information secure?",
                "answer": "Yes, we use SSL encryption and comply with PCI DSS standards to protect your payment information.",
                "category": "payment"
            },
            {
                "question": "How do I reset my password?",
                "answer": "Click on 'Forgot Password' on the login page and follow the instructions sent to your email.",
                "category": "account"
            },
            {
                "question": "Can I change my email address?",
                "answer": "Yes, go to your account settings and update your email address. You'll need to verify it with a confirmation email.",
                "category": "account"
            },
            {
                "question": "What should I do if I receive a damaged product?",
                "answer": "Contact our support team immediately with photos of the damage. We'll arrange a replacement or refund.",
                "category": "product_issue"
            }
        ]
        
        return faqs
    
    @staticmethod
    def save_to_json(data: List[Dict], filename: str, output_dir: str = "./data"):
        """Save data to JSON file"""
        os.makedirs(output_dir, exist_ok=True)
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"✓ Data saved to {filepath}")
    
    @staticmethod
    def save_to_csv(data: List[Dict], filename: str, output_dir: str = "./data"):
        """Save data to CSV file"""
        os.makedirs(output_dir, exist_ok=True)
        filepath = os.path.join(output_dir, filename)
        
        if not data:
            return
        
        with open(filepath, 'w', newline='') as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        
        print(f"✓ Data saved to {filepath}")
    
    @staticmethod
    def generate_all_datasets(output_dir: str = "./data"):
        """Generate all sample datasets"""
        print("Generating sample datasets...")
        
        # Generate tickets
        tickets = SampleDatasetGenerator.generate_tickets(100)
        SampleDatasetGenerator.save_to_json(tickets, "sample_tickets.json", output_dir)
        SampleDatasetGenerator.save_to_csv(tickets, "sample_tickets.csv", output_dir)
        
        # Generate FAQs
        faqs = SampleDatasetGenerator.generate_faqs()
        SampleDatasetGenerator.save_to_json(faqs, "sample_faqs.json", output_dir)
        SampleDatasetGenerator.save_to_csv(faqs, "sample_faqs.csv", output_dir)
        
        print(f"✓ All datasets generated in {output_dir}/")
        
        return {
            "tickets": tickets,
            "faqs": faqs
        }


if __name__ == "__main__":
    generator = SampleDatasetGenerator()
    datasets = generator.generate_all_datasets()
    print(f"\nGenerated {len(datasets['tickets'])} tickets and {len(datasets['faqs'])} FAQs")
