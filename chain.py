import ecdsa
import hashlib
import tkinter as tk
from tkinter import messagebox, simpledialog

class BlockchainAccount:
    def __init__(self, username):
        self.username = username
        self.private_key = self.generate_private_key()
        self.public_key = self.generate_public_key()
        self.address = self.generate_address()
        self.balance = 100  # Default balance of 100 cryptos
        self.tokens_earned = 0  # Tokens earned through transfers
        self.transaction_count = 0  # Count of successful transactions

    def generate_private_key(self):
        return ecdsa.SigningKey.generate(curve=ecdsa.SECP256k1)

    def generate_public_key(self):
        return self.private_key.get_verifying_key()

    def generate_address(self):
        public_key_bytes = self.public_key.to_string()
        sha256_bpk = hashlib.sha256(public_key_bytes).digest()
        ripemd160_bpk = hashlib.new('ripemd160', sha256_bpk).digest()
        return ripemd160_bpk.hex()

    def get_account_details(self):
        return {
            'username': self.username,
            'private_key': self.private_key.to_string().hex(),
            'public_key': self.public_key.to_string().hex(),
            'address': self.address,
            'balance': self.balance,
            'tokens_earned': self.tokens_earned,
            'transaction_count': self.transaction_count
        }

    def transfer(self, recipient, amount):
        fee = amount * 0.003  # 0.3% fee
        total_amount = amount + fee
        if self.balance >= total_amount:
            self.balance -= total_amount
            recipient.balance += amount
            self.balance += 3  # Reward the sender with 3 tokens
            self.tokens_earned += 3  # Track tokens earned
            self.transaction_count += 1
            if self.transaction_count > 10:
                additional_tokens = 2  # 3 (previous) + 2 (increment) = 5
                self.balance += additional_tokens
                self.tokens_earned += additional_tokens
            return True, fee
        else:
            return False, fee

    def redeem_gift_card(self, choice):
        if self.tokens_earned >= 1000:
            self.tokens_earned -= 1000
            gift_card = ["Amazon", "Myntra", "Flipkart", "BookMyShow"][int(choice) - 1]
            return True, gift_card
        else:
            return False, None

class BlockchainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Blockchain Account Management")
        self.accounts = []

        self.create_widgets()

    def create_widgets(self):
        self.description_label = tk.Label(self.root,
                                          text="Token based loyalty program, upon creating the account you get 100 cryptos as default. It's a test program.",
                                          wraplength=400, justify="left")
        self.description_label.pack(pady=10)

        self.create_account_button = tk.Button(self.root, text="Create Account", command=self.create_account)
        self.create_account_button.pack(pady=10)

        self.user_details_button = tk.Button(self.root, text="Check User Details", command=self.check_user_details)
        self.user_details_button.pack(pady=10)

        self.transfer_button = tk.Button(self.root, text="Transfer Cryptos", command=self.transfer_cryptos)
        self.transfer_button.pack(pady=10)

        self.check_balance_button = tk.Button(self.root, text="Check Balance", command=self.check_balance)
        self.check_balance_button.pack(pady=10)

        self.view_tokens_button = tk.Button(self.root, text="View Tokens Earned", command=self.view_tokens_earned)
        self.view_tokens_button.pack(pady=10)

        self.redeem_button = tk.Button(self.root, text="Redeem Gift Card", command=self.redeem_gift_card)
        self.redeem_button.pack(pady=10)

        self.exit_button = tk.Button(self.root, text="Exit", command=self.root.quit)
        self.exit_button.pack(pady=10)

    def create_account(self):
        username = simpledialog.askstring("Input", "Enter username for the account:")
        if username:
            account = BlockchainAccount(username)
            self.accounts.append(account)
            account_details = account.get_account_details()
            messagebox.showinfo("Account Created", f"Account Details:\nUsername: {account_details['username']}\n"
                                                   f"Private Key: {account_details['private_key']}\n"
                                                   f"Public Key: {account_details['public_key']}\n"
                                                   f"Address: {account_details['address']}\n"
                                                   f"Balance: {account_details['balance']} cryptos")

    def find_account(self, username):
        for account in self.accounts:
            if account.username == username:
                return account
        return None

    def transfer_cryptos(self):
        messagebox.showinfo("Transfer Info", "After successful completion of 10 transactions you will get an additional bonus of 2 tokens. Total of 5")
        sender_username = simpledialog.askstring("Input", "Enter the sender's username:")
        recipient_username = simpledialog.askstring("Input", "Enter the recipient's username:")
        amount = simpledialog.askfloat("Input", "Enter the amount to transfer:")

        sender = self.find_account(sender_username)
        recipient = self.find_account(recipient_username)

        if sender and recipient:
            success, fee = sender.transfer(recipient, amount)
            if success:
                messagebox.showinfo("Transfer Successful", f"{sender_username} transferred {amount} cryptos to {recipient_username}.\n"
                                                           f"Gas fee of {fee} cryptos applied.\n"
                                                           f"{sender_username} received a reward of 3 tokens.")
                if sender.transaction_count > 10:
                    messagebox.showinfo("Additional Reward", f"{sender_username} received an additional reward of 2 tokens for completing more than 10 transactions.")
            else:
                messagebox.showerror("Transfer Failed", "Insufficient balance.")
        else:
            messagebox.showerror("Error", "Invalid sender or recipient username.")

    def check_balance(self):
        username = simpledialog.askstring("Input", "Enter the username to check balance:")
        account = self.find_account(username)
        if account:
            messagebox.showinfo("Balance", f"{username}'s balance: {account.balance} cryptos")
        else:
            messagebox.showerror("Error", "Account not found.")

    def view_tokens_earned(self):
        username = simpledialog.askstring("Input", "Enter the username to check tokens earned:")
        account = self.find_account(username)
        if account:
            messagebox.showinfo("Tokens Earned", f"{username} has earned {account.tokens_earned} tokens through transfers.")
        else:
            messagebox.showerror("Error", "Account not found.")

    def redeem_gift_card(self):
        username = simpledialog.askstring("Input", "Enter the username to redeem gift card:")
        account = self.find_account(username)
        if account:
            choice = simpledialog.askstring("Input", "Choose a gift card to redeem:\n1. Amazon\n2. Myntra\n3. Flipkart\n4. BookMyShow")
            if choice in ['1', '2', '3', '4']:
                success, gift_card = account.redeem_gift_card(choice)
                if success:
                    messagebox.showinfo("Redeem Successful", f"{username} has successfully redeemed a {gift_card} gift card worth 1000 tokens.")
                else:
                    messagebox.showerror("Redeem Failed", f"{username} does not have enough tokens to redeem a gift card.")
            else:
                messagebox.showerror("Error", "Invalid choice. No gift card redeemed.")
        else:
            messagebox.showerror("Error", "Account not found.")

    def check_user_details(self):
        username = simpledialog.askstring("Input", "Enter the username to check details:")
        account = self.find_account(username)
        if account:
            account_details = account.get_account_details()
            messagebox.showinfo("User Details", f"Username: {account_details['username']}\n"
                                                f"Private Key: {account_details['private_key']}\n"
                                                f"Public Key: {account_details['public_key']}\n"
                                                f"Address: {account_details['address']}\n"
                                                f"Balance: {account_details['balance']} cryptos\n"
                                                f"Tokens Earned: {account_details['tokens_earned']}\n"
                                                f"Transaction Count: {account_details['transaction_count']}")
        else:
            messagebox.showerror("Error", "Account not found.")

if __name__ == "__main__":
    root = tk.Tk()
    app = BlockchainApp(root)
    root.mainloop()
