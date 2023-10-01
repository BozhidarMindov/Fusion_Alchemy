import { Component } from '@angular/core';
import { HttpClient } from '@angular/common/http';


@Component({
  selector: 'app-homepage',
  templateUrl: './homepage.component.html',
  styleUrls: ['./homepage.component.scss']
})
export class HomepageComponent {
  userName: string = '';
  avatarImage: string | null = null;

  constructor(private http: HttpClient) {}

  generateAvatar() {
    if (this.userName.trim() === '') {
      // Handle empty name input (you can display an error message)
      return;
    }

    // Send the user's name to the backend to generate the avatar
    this.http.post<any>('http://localhost:8000/generate', { "name": this.userName }).subscribe(
      (response) => {
        // Assuming the backend responds with the URL of the generated image
        this.avatarImage = response.path;
      },
      (error) => {
        console.error('Error generating avatar:', error);
        // Handle error (display an error message, if needed)
      }
    );
  }
}
