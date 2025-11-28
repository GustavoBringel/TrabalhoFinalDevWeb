import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ServicoListPage } from './servico-list.page';

describe('ServicoListPage', () => {
  let component: ServicoListPage;
  let fixture: ComponentFixture<ServicoListPage>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ServicoListPage],
    }).compileComponents();

    fixture = TestBed.createComponent(ServicoListPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
