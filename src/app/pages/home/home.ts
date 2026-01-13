import { Component } from '@angular/core';
import { RouterLink } from '@angular/router';
import { About } from '../about/about';
import { Skills } from '../skills/skills';
import { Experience } from '../experience/experience';
import { Projects } from '../projects/projects';
import { Contact } from '../contact/contact';

@Component({
  selector: 'app-home',
  imports: [RouterLink, About, Skills, Experience, Projects, Contact],
  templateUrl: './home.html',
  styleUrl: './home.css',
})
export class Home {

}
