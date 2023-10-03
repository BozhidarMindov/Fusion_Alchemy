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
  loading: boolean = false; // Initialize the loading variable

  // Store the last used username for regeneration
  lastUsedUserName: string | null = null;

  constructor(private http: HttpClient) {}

  generateAvatar() {
    if (this.userName.trim() === '') {
      // Handle empty name input (you can display an error message)
      return;
    }

    // Set loading to true to show the loading indicator
    this.loading = true;

    // Store the last used username
    this.lastUsedUserName = this.userName;

    // Send the user's name to the backend to generate the avatar
    this.http.post<any>('http://localhost:8000/generate', { "name": this.userName }).subscribe(
      (response) => {
        // Assuming the backend responds with the URL of the generated image
        this.avatarImage = response.path;

        // Set loading back to false when the operation is complete
        this.loading = false;
      },
      (error) => {
        // Handle error (display an error message, if needed)
        console.error('Error generating avatar:', error)

        // Set loading back to false in case of an error
        this.loading = false;
      }
    );
  }

  regenerateAvatar() {
    if (this.lastUsedUserName) {
      // Use the last used username for regeneration
      this.userName = this.lastUsedUserName;
      // Set teh current avatar image to '' to make the previous image disappear.
      this.avatarImage = ''
      this.generateAvatar(); // Reuse the generateAvatar function
    } else {
      // Handle case where there's no previous username to regenerate
      console.error('Error generating avatar');
    }
  }

  downloadAvatar() {
    if (this.avatarImage) {
      // Convert the avatar image URL to a blob
      fetch(this.avatarImage)
        .then(response => response.blob())
        .then(blob => {
          // Create an object URL from the blob
          const blobURL = URL.createObjectURL(blob);

          // Create an anchor element to trigger the download
          const link = document.createElement('a');
          link.href = blobURL;
          link.download = 'avatar.png'; // Set the filename for download
          link.click();

          // Release the object URL to free resources
          URL.revokeObjectURL(blobURL);
        })
        .catch(error => {
          console.error('Error generating avatar:', error);
        });
    } else {
      // Handle case where there's no avatar image to download
      console.error('Error generating avatar');
    }
  }
}
