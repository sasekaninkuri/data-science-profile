import { Routes } from '@angular/router';
import { Home } from './pages/home/home';
import { About } from './pages/about/about';
import { Skills } from './pages/skills/skills';
import { Experience } from './pages/experience/experience';
import { Projects } from './pages/projects/projects';
import { Contact } from './pages/contact/contact';

export const routes: Routes = [
    { path: '', component: Home },
    { path: 'about', component: About },
    { path: 'skills', component: Skills },
    { path: 'experience', component: Experience },
    { path: 'projects', component: Projects },
    { path: 'contact', component: Contact },
    { path: '**', redirectTo: '' }
];
