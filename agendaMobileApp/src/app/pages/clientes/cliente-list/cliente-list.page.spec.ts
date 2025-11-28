import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ClienteListPage } from './cliente-list.page';

describe('ClienteListPage', () => {
  let component: ClienteListPage;
  let fixture: ComponentFixture<ClienteListPage>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ClienteListPage],
    }).compileComponents();

    fixture = TestBed.createComponent(ClienteListPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
