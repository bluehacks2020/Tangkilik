import { TestBed } from '@angular/core/testing';

import { MainControllerService } from './main-controller.service';

describe('MainControllerService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: MainControllerService = TestBed.get(MainControllerService);
    expect(service).toBeTruthy();
  });
});
