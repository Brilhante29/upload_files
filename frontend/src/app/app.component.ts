import { Component, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html'
})
export class AppComponent implements OnInit {
  file?: File;
  etags: {ETag: string, PartNumber: number}[] = [];
  uploadId = '';
  key = '';
  apiUrl = '';

  constructor(private http: HttpClient) {}

  ngOnInit() {
    this.http.get<{apiUrl: string}>('/config').subscribe(cfg => this.apiUrl = cfg.apiUrl);
  }

  onFileChange(event: any) {
    this.file = event.target.files[0];
  }

  async upload() {
    if (!this.file || !this.apiUrl) return;
    const startResp = await this.http.post<any>(`${this.apiUrl}/start`, {}).toPromise();
    this.uploadId = startResp.uploadId;
    this.key = startResp.key;
    const chunkSize = 5 * 1024 * 1024;
    const totalParts = Math.ceil(this.file.size / chunkSize);
    for (let part = 1; part <= totalParts; part++) {
      const start = (part - 1) * chunkSize;
      const end = Math.min(this.file.size, part * chunkSize);
      const blob = this.file.slice(start, end);
      const etagResp = await this.http.put<any>(`${this.apiUrl}/part?uploadId=${this.uploadId}&partNumber=${part}&key=${this.key}`, blob, {
        headers: {'Content-Type': 'application/octet-stream'}
      }).toPromise();
      this.etags.push({ETag: etagResp.ETag, PartNumber: part});
    }
    await this.http.post(`${this.apiUrl}/complete`, {
      uploadId: this.uploadId,
      key: this.key,
      parts: this.etags
    }).toPromise();
    alert('Upload complete');
  }
}
