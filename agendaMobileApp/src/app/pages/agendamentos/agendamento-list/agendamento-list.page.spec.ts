import { ComponentFixture, TestBed } from '@angular/core/testing';
import { AgendamentoListPage } from './agendamento-list.page';

describe('AgendamentoListPage', () => {
  let component: AgendamentoListPage;
  let fixture: ComponentFixture<AgendamentoListPage>;

  beforeEach(() => {
    fixture = TestBed.createComponent(AgendamentoListPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
