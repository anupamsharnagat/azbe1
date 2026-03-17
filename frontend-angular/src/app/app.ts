import { Component, inject, signal, ViewChild, ElementRef, AfterViewChecked } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { RagService } from './rag.service';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './app.html',
  styleUrl: './app.css'
})
export class App implements AfterViewChecked {
  @ViewChild('chatBox') private chatBox!: ElementRef;
  private ragService = inject(RagService);

  messages = signal<{role: string, text: string}[]>([]);
  userInput = signal('');
  isProcessing = signal(false);
  isUploaded = signal(false);
  fileName = signal('');

  ngAfterViewChecked() {
    this.scrollToBottom();
  }

  onFileSelected(event: any) {
    const file: File = event.target.files[0];
    if (file) {
      this.isProcessing.set(true);
      this.fileName.set(file.name);
      
      this.ragService.upload(file).subscribe({
        next: (res: any) => {
          this.isUploaded.set(true);
          this.messages.update(m => [...m, { role: 'ai', text: `Successfully indexed "${file.name}". You can now ask questions about the document.` }]);
          this.isProcessing.set(false);
        },
        error: (err: any) => {
          alert('Upload failed: ' + (err.error?.detail || err.message));
          this.isProcessing.set(false);
        }
      });
    }
  }

  send() {
    const q = this.userInput().trim();
    if (!q || this.isProcessing() || !this.isUploaded()) return;

    this.messages.update(m => [...m, { role: 'user', text: q }]);
    this.userInput.set('');
    this.isProcessing.set(true);

    this.ragService.ask(q).subscribe({
      next: (res: any) => {
        this.messages.update(m => [...m, { role: 'ai', text: res.answer }]);
        this.isProcessing.set(false);
      },
      error: (err: any) => {
        alert('Query failed: ' + (err.error?.detail || err.message));
        this.isProcessing.set(false);
      }
    });
  }

  private scrollToBottom(): void {
    try {
      this.chatBox.nativeElement.scrollTop = this.chatBox.nativeElement.scrollHeight;
    } catch (err) {}
  }
}
