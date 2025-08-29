import * as React from 'react';
import ArcherElement from '../ArcherElement';
import { RelationType } from '../../types';
import { fireEvent, render } from '@testing-library/react';
import { ArcherContainerContextProvider } from '../../ArcherContainer/ArcherContainer.context';

describe('ArcherElement', () => {
  let registerChildMock: jest.Mock<any, any>;
  let unregisterChildMock: jest.Mock<any, any>;
  let registerTransitionsMock: jest.Mock<any, any>;
  let unregisterTransitionsMock: jest.Mock<any, any>;

  const children = <div>hi</div>;
  const defaultProps = {
    relations: [],
    id: '',
    children,
  };

  type MockArcherContainerType = {
    registerTransitions: (...args: Array<any>) => any;
    unregisterTransitions: (...args: Array<any>) => any;
    registerChild: (...args: Array<any>) => any;
    unregisterChild: (...args: Array<any>) => any;
    children: React.ReactNode;
  };

  const MockArcherContainer = ({
    registerTransitions,
    unregisterTransitions,
    registerChild,
    unregisterChild,
    children,
  }: MockArcherContainerType) => (
    <ArcherContainerContextProvider
      value={{
        registerTransitions,
        unregisterTransitions,
        registerChild,
        unregisterChild,
      }}
    >
      {children}
    </ArcherContainerContextProvider>
  ); // For triggering relations props changes in a less contrived way

  class PassThrough extends React.Component<
    { relations: RelationType[]; newRelations: RelationType[]; id: string },
    any
  > {
    state = {
      relations: this.props.relations,
      newRelations: this.props.newRelations,
    };

    render() {
      const { relations, newRelations } = this.state;
      return (
        <ArcherElement {...this.props} relations={relations}>
          <div
            className="foo"
            onClick={() =>
              this.setState({
                relations: newRelations,
              })
            }
          >
            Update relations
          </div>
        </ArcherElement>
      );
    }
  }

  const mountContainer = (relations: Array<RelationType>, newRelations: Array<RelationType>) => {
    const props = { ...defaultProps, id: 'dumb-id' };
    return render(
      <MockArcherContainer
        registerChild={registerChildMock}
        unregisterChild={unregisterChildMock}
        registerTransitions={registerTransitionsMock}
        unregisterTransitions={unregisterTransitionsMock}
      >
        <PassThrough {...props} relations={relations} newRelations={newRelations} />
      </MockArcherContainer>,
    );
  };

  beforeEach(() => {
    registerChildMock = jest.fn();
    unregisterChildMock = jest.fn();
    registerTransitionsMock = jest.fn();
    unregisterTransitionsMock = jest.fn();
  });

  it('should register and unregister child on mounting ref callback', () => {
    const relations: RelationType[] = [];
    const wrapper = mountContainer(relations, []);
    // See we register the child
    expect(registerChildMock).toHaveBeenCalledWith('dumb-id', expect.anything());
    wrapper.unmount();
    // See we unregister the child and all transitions
    expect(unregisterChildMock).toHaveBeenCalledWith('dumb-id');
    expect(unregisterTransitionsMock).toHaveBeenCalledWith('dumb-id');
    expect(registerChildMock).toHaveBeenCalledTimes(1);
    expect(unregisterChildMock).toHaveBeenCalledTimes(1);
    expect(unregisterTransitionsMock).toHaveBeenCalledTimes(1);
  });

  describe('lifecycle', () => {
    it('should call registerTransitions with sourceToTargets on mount if relations', () => {
      const relations: RelationType[] = [
        {
          targetId: 'toto',
          targetAnchor: 'top',
          sourceAnchor: 'left',
        },
      ];
      const sourceToTargets = [
        {
          source: {
            id: 'dumb-id',
            anchor: 'left',
          },
          target: {
            id: 'toto',
            anchor: 'top',
          },
          order: 0,
          label: undefined,
          style: undefined,
        },
      ];
      mountContainer(relations, []);
      expect(registerTransitionsMock).toHaveBeenCalledWith('dumb-id', sourceToTargets);
    });

    it('should call registerTransitions with proper sourceToTargets when relations change', () => {
      const relations: RelationType[] = [
        {
          targetId: 'toto',
          targetAnchor: 'top',
          sourceAnchor: 'right',
        },
      ];
      const newRelations: RelationType[] = [
        {
          targetId: 'toto',
          targetAnchor: 'top',
          sourceAnchor: 'left',
        },
      ];
      const sourceToTargets = [
        {
          source: {
            id: 'dumb-id',
            anchor: 'left',
          },
          target: {
            id: 'toto',
            anchor: 'top',
          },
          order: 0,
          label: undefined,
          style: undefined,
        },
      ];
      const wrapper = mountContainer(relations, newRelations);
      // Trigger update in ArcherElement
      fireEvent.click(wrapper.getByText('Update relations'));
      expect(registerTransitionsMock).toHaveBeenCalledWith('dumb-id', sourceToTargets);
    });

    it('should not call unregisterTransitions and registerTransitions when relation is the same', () => {
      const relations: RelationType[] = [
        {
          targetId: 'toto',
          targetAnchor: 'top',
          sourceAnchor: 'left',
        },
      ];
      const newRelations: RelationType[] = [
        {
          targetId: 'toto',
          targetAnchor: 'top',
          sourceAnchor: 'left',
        },
      ];
      const wrapper = mountContainer(relations, newRelations);
      // Will get called on mount regardless
      registerTransitionsMock.mockReset();
      // Trigger update in ArcherElement
      fireEvent.click(wrapper.getByText('Update relations'));
      expect(unregisterTransitionsMock).not.toHaveBeenCalled();
      expect(registerTransitionsMock).not.toHaveBeenCalled();
    });

    it('should still call registerTransitions on mount even if no relations', () => {
      const relations: RelationType[] = [];
      mountContainer(relations, []);
      expect(registerTransitionsMock).toHaveBeenCalled();
    });
  });
});
